from sentence_transformers import SentenceTransformer


class MultilingualEmbedder:
    """
    Generates multilingual sentence embeddings.

    The selected model maps semantically similar sentences
    from different languages into a comparable vector space.
    """

    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self):
        print(f"Loading multilingual embedding model: {self.MODEL_NAME}")

        self.model = SentenceTransformer(self.MODEL_NAME)

        print("Multilingual embedding model loaded successfully.")

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def encode_single(self, text: str):
        return self.encode([text])[0]