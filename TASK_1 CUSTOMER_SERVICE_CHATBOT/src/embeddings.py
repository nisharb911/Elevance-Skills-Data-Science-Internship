from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Load embedding model
# ---------------------------------------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ---------------------------------------------------------
# Generate embedding
# ---------------------------------------------------------

def create_embedding(text: str):

    """
    Convert text into a numerical vector.

    Parameters
    ----------
    text : str
        Input text.

    Returns
    -------
    vector
        Numerical representation of the text.
    """

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    text = "What is your refund policy?"

    embedding = create_embedding(text)

    print("\nText:")
    print(text)

    print("\nEmbedding shape:")
    print(embedding.shape)

    print("\nFirst 10 values:")
    print(embedding[:10])

