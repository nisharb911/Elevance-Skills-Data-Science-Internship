from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded successfully.")

    def generate_embeddings(self, texts):
        """Generate embeddings for a list of text chunks."""

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings