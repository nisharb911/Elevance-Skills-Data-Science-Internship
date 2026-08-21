import numpy as np

from .embeddings import create_embedding


# ---------------------------------------------------------
# Calculate cosine similarity
# ---------------------------------------------------------

def cosine_similarity(
    vector_a,
    vector_b
) -> float:
    """
    Calculate cosine similarity between two vectors.

    Returns a value approximately between -1 and 1.
    Higher values indicate greater similarity.
    """

    vector_a = np.asarray(vector_a)
    vector_b = np.asarray(vector_b)

    similarity = np.dot(
        vector_a,
        vector_b
    )

    return float(similarity)


# ---------------------------------------------------------
# Test semantic similarity
# ---------------------------------------------------------

if __name__ == "__main__":

    texts = [
        "What is your refund policy?",
        "How can I get my money back?",
        "What payment methods do you accept?",
        "How long does delivery take?"
    ]


    # Create embeddings
    embeddings = [
        create_embedding(text)
        for text in texts
    ]


    print("\nSemantic Similarity Results")
    print("=" * 60)


    # Compare first sentence with every other sentence

    reference_text = texts[0]
    reference_embedding = embeddings[0]


    print(f"\nReference:")
    print(reference_text)


    for text, embedding in zip(
        texts[1:],
        embeddings[1:]
    ):

        score = cosine_similarity(
            reference_embedding,
            embedding
        )

        print("\nCompared with:")
        print(text)

        print(
            f"Similarity: {score:.4f}"
        )

