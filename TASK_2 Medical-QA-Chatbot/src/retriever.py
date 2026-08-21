"""
MedQuAD Medical Semantic Search
Hybrid Retrieval Version

This version fixes two problems:
1. It uses the actual project index: models/medical_qa.index
2. It combines semantic similarity with keyword/phrase matching so
   questions such as:
       "What is insulin used for?"
       "What are the symptoms of arthritis?"
   are less likely to return loosely related diseases.

It does NOT require rebuilding the existing FAISS index.
"""

from pathlib import Path
import math
import pickle
import re
import sys
from collections import Counter

import faiss
from sentence_transformers import SentenceTransformer


# ================================================================
# PROJECT PATHS
# ================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "models" / "medical_qa.index"
METADATA_PATH = BASE_DIR / "models" / "qa_metadata.pkl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ================================================================
# TEXT UTILITIES
# ================================================================

STOP_WORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "be", "been", "being", "do", "does", "did",
    "what", "which", "who", "whom", "where", "when", "why", "how",
    "can", "could", "would", "should", "may", "might",
    "for", "of", "to", "in", "on", "at", "by", "with", "from",
    "and", "or", "as", "about", "tell", "me",
    "used", "use", "please"
}


def tokenize(text):
    """Convert text into useful lowercase word tokens."""
    return [
        token
        for token in re.findall(r"[a-zA-Z0-9]+", str(text).lower())
        if token not in STOP_WORDS and len(token) > 1
    ]


def normalize_text(text):
    return re.sub(
        r"\s+",
        " ",
        str(text).strip().lower()
    )


# ================================================================
# MEDICAL RETRIEVER
# ================================================================

class MedicalRetriever:

    def __init__(
        self,
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH,
        model_name=MODEL_NAME
    ):

        print("Loading medical retrieval system...")

        if not Path(index_path).exists():
            raise FileNotFoundError(
                f"FAISS index not found:\n{index_path}\n\n"
                "Expected file:\n"
                "models\\medical_qa.index"
            )

        if not Path(metadata_path).exists():
            raise FileNotFoundError(
                f"Metadata file not found:\n{metadata_path}"
            )

        # ----------------------------------------------------------
        # Sentence Transformer
        # ----------------------------------------------------------

        self.model = SentenceTransformer(model_name)

        # ----------------------------------------------------------
        # FAISS
        # ----------------------------------------------------------

        self.index = faiss.read_index(str(index_path))

        # ----------------------------------------------------------
        # Metadata
        # ----------------------------------------------------------

        with open(metadata_path, "rb") as file:
            self.metadata = pickle.load(file)

        self.questions = [
            str(q)
            for q in self.metadata["questions"]
        ]

        self.answers = self.metadata["answers"]

        # ----------------------------------------------------------
        # Pre-tokenize questions for fast lexical matching
        # ----------------------------------------------------------

        self.question_tokens = [
            set(tokenize(question))
            for question in self.questions
        ]

        # Document frequency for simple IDF weighting
        document_frequency = Counter()

        for tokens in self.question_tokens:
            document_frequency.update(tokens)

        total_documents = max(len(self.question_tokens), 1)

        self.idf = {
            token: math.log(
                (total_documents + 1)
                / (frequency + 1)
            ) + 1.0
            for token, frequency in document_frequency.items()
        }

        print("Medical retrieval system loaded.")
        print(f"Indexed questions: {self.index.ntotal}")

    # ==============================================================
    # LEXICAL SCORE
    # ==============================================================

    def lexical_score(self, query_tokens, question_index):
        """
        Calculate weighted keyword overlap.

        Rare medical terms such as 'influenza', 'insulin',
        'arthritis', etc. receive more importance than common words.
        """

        if not query_tokens:
            return 0.0

        question_tokens = self.question_tokens[question_index]

        if not question_tokens:
            return 0.0

        matched = query_tokens.intersection(question_tokens)

        if not matched:
            return 0.0

        query_weight = sum(
            self.idf.get(token, 1.0)
            for token in query_tokens
        )

        matched_weight = sum(
            self.idf.get(token, 1.0)
            for token in matched
        )

        if query_weight == 0:
            return 0.0

        return matched_weight / query_weight

    # ==============================================================
    # SEARCH
    # ==============================================================

    def search(
        self,
        query,
        top_k=5,
        min_score=None
    ):
        """
        Hybrid medical search.

        Step 1:
            Semantic search with FAISS.

        Step 2:
            Keyword search over all MedQuAD questions.

        Step 3:
            Combine semantic + lexical scores.

        Step 4:
            Remove duplicate questions.

        This makes the retriever much more robust for exact medical
        terms while keeping semantic understanding.
        """

        query = str(query).strip()

        if not query:
            return []

        query_tokens = set(tokenize(query))

        # ----------------------------------------------------------
        # Semantic search
        # ----------------------------------------------------------

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Retrieve a large semantic candidate pool.
        semantic_k = min(
            max(top_k * 20, 100),
            self.index.ntotal
        )

        semantic_scores, semantic_indices = self.index.search(
            query_embedding,
            semantic_k
        )

        candidate_indices = set()

        for index in semantic_indices[0]:
            if index >= 0:
                candidate_indices.add(int(index))

        # ----------------------------------------------------------
        # Lexical candidate search
        #
        # Scan the question list so a question containing an exact
        # medical term can enter the candidate pool even if its
        # embedding score is unexpectedly low.
        # ----------------------------------------------------------

        lexical_candidates = []

        if query_tokens:

            for index in range(len(self.questions)):

                score = self.lexical_score(
                    query_tokens,
                    index
                )

                if score > 0:
                    lexical_candidates.append(
                        (score, index)
                    )

            lexical_candidates.sort(
                key=lambda item: item[0],
                reverse=True
            )

            # Add enough lexical candidates for reranking.
            lexical_limit = min(
                max(top_k * 20, 100),
                len(lexical_candidates)
            )

            for _, index in lexical_candidates[:lexical_limit]:
                candidate_indices.add(index)

        # ----------------------------------------------------------
        # Build semantic score lookup
        # ----------------------------------------------------------

        semantic_score_map = {}

        for score, index in zip(
            semantic_scores[0],
            semantic_indices[0]
        ):
            if index >= 0:
                semantic_score_map[int(index)] = float(score)

        # ----------------------------------------------------------
        # Score every candidate
        # ----------------------------------------------------------

        ranked = []

        for index in candidate_indices:

            semantic_score = semantic_score_map.get(
                index,
                0.0
            )

            lexical_score = self.lexical_score(
                query_tokens,
                index
            )

            question = normalize_text(
                self.questions[index]
            )

            normalized_query = normalize_text(query)

            # Exact phrase bonus
            phrase_bonus = 0.0

            if normalized_query in question:
                phrase_bonus = 0.25

            # Strong medical-term bonus.
            # This helps "insulin" match insulin questions.
            medical_term_bonus = min(
                lexical_score * 0.30,
                0.30
            )

            # Hybrid score
            final_score = (
                (semantic_score * 0.60)
                + (lexical_score * 0.40)
                + phrase_bonus
                + medical_term_bonus
            )

            if min_score is not None and final_score < min_score:
                continue

            ranked.append(
                (
                    final_score,
                    semantic_score,
                    lexical_score,
                    index
                )
            )

        # ----------------------------------------------------------
        # Sort
        # ----------------------------------------------------------

        ranked.sort(
            key=lambda item: item[0],
            reverse=True
        )

        # ----------------------------------------------------------
        # Remove duplicate questions
        # ----------------------------------------------------------

        results = []
        seen_questions = set()

        for (
            final_score,
            semantic_score,
            lexical_score,
            index
        ) in ranked:

            question_text = self.questions[index]

            normalized_question = normalize_text(
                question_text
            )

            if normalized_question in seen_questions:
                continue

            seen_questions.add(
                normalized_question
            )

            result = {
                "rank": len(results) + 1,
                "score": final_score,
                "semantic_score": semantic_score,
                "lexical_score": lexical_score,
                "question": question_text,
                "answer": self.answers[index],
                "question_id": self.metadata["question_ids"][index],
                "focus": self.metadata["focus"][index],
                "question_type": self.metadata["question_type"][index],
                "synonyms": self.metadata["synonyms"][index],
                "source": self.metadata["source"][index],
                "source_file": self.metadata["source_file"][index],
                "url": self.metadata["url"][index]
            }

            results.append(result)

            if len(results) >= top_k:
                break

        return results


# ================================================================
# DISPLAY
# ================================================================

def display_results(results):

    print()
    print("=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    if not results:
        print("No relevant results found.")
        return

    for result in results:

        print()
        print(f"Rank: {result['rank']}")
        print(
            f"Hybrid Score: {result['score']:.4f}"
        )
        print(
            f"Semantic Score: {result['semantic_score']:.4f}"
        )
        print(
            f"Keyword Score: {result['lexical_score']:.4f}"
        )
        print()

        print("Matched Question:")
        print(result["question"])
        print()

        print("Answer:")
        print(result["answer"])
        print()

        print(f"Source: {result['source']}")
        print("-" * 70)


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 70)
    print("MedQuAD Medical Hybrid Semantic Search")
    print("Type 'exit' to stop.")
    print("=" * 70)

    # ----------------------------------------------------------
    # File checks
    # ----------------------------------------------------------

    if not INDEX_PATH.exists():

        print()
        print("ERROR: FAISS index not found.")
        print()
        print("Expected:")
        print(INDEX_PATH)
        print()
        print("Your models folder should contain:")
        print("  medical_qa.index")
        print("  qa_metadata.pkl")
        print()
        sys.exit(1)

    if not METADATA_PATH.exists():

        print()
        print("ERROR: Metadata file not found.")
        print()
        print("Expected:")
        print(METADATA_PATH)
        print()
        sys.exit(1)

    # ----------------------------------------------------------
    # Load
    # ----------------------------------------------------------

    try:

        retriever = MedicalRetriever()

    except Exception as error:

        print()
        print("ERROR while loading retrieval system:")
        print(error)
        print()
        sys.exit(1)

    # ----------------------------------------------------------
    # Interactive loop
    # ----------------------------------------------------------

    while True:

        try:
            query = input(
                "\nEnter your medical question: "
            ).strip()

        except (KeyboardInterrupt, EOFError):

            print("\nExiting...")
            break

        if query.lower() == "exit":

            print("\nExiting...")
            break

        if not query:

            print("Please enter a medical question.")
            continue

        try:

            results = retriever.search(
                query,
                top_k=5
            )

            display_results(results)

        except Exception as error:

            print()
            print("ERROR during search:")
            print(error)


if __name__ == "__main__":
    main()