import numpy as np

from .knowledge_base import load_knowledge_base
from .embeddings import create_embedding


# =========================================================
# Configuration
# =========================================================

DEFAULT_TOP_K = 2

# Minimum semantic similarity required for a result.
# This prevents completely unrelated FAQ sections
# from being returned.
RELEVANCE_THRESHOLD = 0.30


# =========================================================
# Load Knowledge Base
# =========================================================

KNOWLEDGE = load_knowledge_base()


# =========================================================
# Split Knowledge Base into Sections
# =========================================================

def split_into_sections(text: str) -> list[str]:
    """
    Split the company knowledge base into sections.

    Each section starts with a Markdown heading:

    ## Payments
    ## Refunds
    ## Returns
    """

    sections = text.strip().split("\n## ")

    cleaned_sections = []

    for index, section in enumerate(sections):

        if index > 0:
            section = "## " + section

        section = section.strip()

        if section:
            cleaned_sections.append(section)

    return cleaned_sections


# =========================================================
# Prepare Knowledge Base Sections
# =========================================================

SECTIONS = split_into_sections(KNOWLEDGE)


# =========================================================
# Create Knowledge Base Embeddings
# =========================================================

print("Creating knowledge-base embeddings...")

SECTION_EMBEDDINGS = np.array(
    [
        create_embedding(section)
        for section in SECTIONS
    ]
)

print(
    f"Created embeddings for {len(SECTIONS)} sections."
)


# =========================================================
# Semantic Retrieval
# =========================================================

def retrieve_information(
    user_query: str,
    top_k: int = DEFAULT_TOP_K
) -> str:
    """
    Retrieve relevant company information using
    semantic similarity.

    Parameters
    ----------
    user_query : str
        Customer question.

    top_k : int
        Number of relevant sections to return.

    Returns
    -------
    str
        Relevant knowledge-base information.
    """

    if not user_query or not user_query.strip():

        return (
            "No relevant information was found "
            "in the company knowledge base."
        )

    # -----------------------------------------------------
    # Create embedding for customer query
    # -----------------------------------------------------

    query_embedding = create_embedding(
        user_query
    )

    # -----------------------------------------------------
    # Calculate cosine similarity
    #
    # Embeddings are normalized, therefore dot product
    # gives cosine similarity.
    # -----------------------------------------------------

    similarities = np.dot(
        SECTION_EMBEDDINGS,
        query_embedding
    )

    # -----------------------------------------------------
    # Get highest similarity indexes
    # -----------------------------------------------------

    top_indexes = np.argsort(
        similarities
    )[::-1]

    # -----------------------------------------------------
    # Select relevant sections
    # -----------------------------------------------------

    selected_sections = []

    for index in top_indexes:

        score = float(
            similarities[index]
        )

        # Ignore unrelated information
        if score < RELEVANCE_THRESHOLD:
            continue

        selected_sections.append(
            (
                score,
                SECTIONS[index]
            )
        )

        if len(selected_sections) >= top_k:
            break

    # -----------------------------------------------------
    # No sufficiently relevant information
    # -----------------------------------------------------

    if not selected_sections:

        return (
            "No sufficiently relevant information was found "
            "in the company knowledge base. "
            "Do not invent information."
        )

    # -----------------------------------------------------
    # Format results
    # -----------------------------------------------------

    results = []

    for score, section in selected_sections:

        results.append(
            f"[Relevance: {score:.4f}]\n{section}"
        )

    return "\n\n".join(results)


# =========================================================
# Test Semantic Retrieval
# =========================================================

if __name__ == "__main__":

    test_questions = [

        "What payment methods do you accept?",

        "How long does delivery take?",

        "What is the refund policy?",

        "When can I return a product?",

        "How can I get my money back?",

        "My package hasn't arrived yet.",

        "Can I pay using UPI?"

    ]

    for question in test_questions:

        print("\n" + "=" * 70)

        print("Customer question:")
        print(question)

        print("\nSemantic search results:")

        print(
            retrieve_information(
                question,
                top_k=2
            )
        )