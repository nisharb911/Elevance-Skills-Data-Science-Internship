import re

from src.retriever import ResearchRetriever
from src.llm_generator import ResearchLLM


class ResearchRAG:

    def __init__(self, top_k=5, min_similarity=0.60):

        print("=" * 70)
        print("INITIALIZING RESEARCH RAG")
        print("=" * 70)

        self.top_k = top_k
        self.min_similarity = min_similarity

        print("\nLoading retriever...")
        self.retriever = ResearchRetriever()

        print("\nLoading LLM...")
        self.llm = ResearchLLM()

        print("\nRAG configuration:")
        print(f"  Top K              : {self.top_k}")
        print(f"  Minimum similarity : {self.min_similarity}")

        print("\nRAG pipeline ready.")

    def _extract_keywords(self, question):
        """
        Extract meaningful words from the user question.

        Common English question words are removed because they
        are not useful for determining research-topic relevance.
        """

        stop_words = {
            "what", "what's", "whats",
            "how", "why", "when", "where", "who",
            "which", "are", "is", "was", "were",
            "do", "does", "did",
            "can", "could", "would", "should",
            "the", "a", "an",
            "of", "for", "to", "in", "on", "with",
            "and", "or", "from", "by", "about",
            "used", "use", "using",
            "main", "role", "related",
            "tell", "me", "explain", "describe"
        }

        words = re.findall(
            r"[a-zA-Z][a-zA-Z-]{2,}",
            question.lower()
        )

        return [
            word
            for word in words
            if word not in stop_words
        ]

    def _has_topic_evidence(self, question, results):
        """
        Check whether the retrieved research actually contains
        meaningful terms from the user's question.

        This protects against semantically similar but
        topically unrelated papers.
        """

        query_keywords = self._extract_keywords(question)

        if not query_keywords:
            return True

        # Combine metadata and research text from retrieved papers.
        research_text = ""

        for result in results:

            research_text += " "

            research_text += str(
                result.get("title", "")
            )

            research_text += " "

            research_text += str(
                result.get("keywords", [])
            )

            research_text += " "

            research_text += str(
                result.get("technical_terms", [])
            )

            research_text += " "

            research_text += str(
                result.get("text", "")
            )

        research_text = research_text.lower()

        # Count meaningful question terms found in the research.
        matched_keywords = 0

        for keyword in query_keywords:

            if keyword in research_text:
                matched_keywords += 1

        # At least one important topic term must be supported.
        #
        # For multi-topic questions, require at least 2 matches
        # when the question contains many meaningful terms.
        if len(query_keywords) >= 4:

            return matched_keywords >= 2

        return matched_keywords >= 1

    def retrieve_context(self, question):

        results = self.retriever.search(
            query=question,
            top_k=self.top_k
        )

        # ---------------------------------------------------------
        # STEP 1: Similarity filtering
        # ---------------------------------------------------------

        filtered_results = [
            result
            for result in results
            if result.get("score", 0) >= self.min_similarity
        ]

        if not filtered_results:
            return [], ""

        # ---------------------------------------------------------
        # STEP 2: Topic/evidence verification
        # ---------------------------------------------------------

        if not self._has_topic_evidence(
            question,
            filtered_results
        ):

            return [], ""

        # ---------------------------------------------------------
        # STEP 3: Build research context
        # ---------------------------------------------------------

        context_parts = []

        for i, result in enumerate(
            filtered_results,
            start=1
        ):

            context_parts.append(
                f"""
SOURCE {i}

Paper ID:
{result.get("paper_id", "Unknown")}

Title:
{result.get("title", "Unknown")}

Categories:
{result.get("categories", [])}

Year:
{result.get("year", "Unknown")}

Keywords:
{result.get("keywords", [])}

Technical Terms:
{result.get("technical_terms", [])}

Similarity Score:
{result.get("score", 0):.4f}

Research Text:
{result.get("text", "")}
"""
            )

        context = "\n".join(context_parts)

        return filtered_results, context

    def ask(
        self,
        question,
        conversation_history=None
    ):

        results, context = self.retrieve_context(
            question
        )

        # ---------------------------------------------------------
        # No sufficiently reliable evidence
        # ---------------------------------------------------------

        if not results:

            return {
                "question": question,
                "answer": (
                    "I could not find sufficiently relevant research "
                    "in the available arXiv dataset to answer this "
                    "question reliably."
                ),
                "sources": []
            }

        # ---------------------------------------------------------
        # Generate answer using verified research context
        # ---------------------------------------------------------

        answer = self.llm.generate_answer(
            question=question,
            context=context,
            conversation_history=conversation_history
        )

        return {
            "question": question,
            "answer": answer,
            "sources": results
        }