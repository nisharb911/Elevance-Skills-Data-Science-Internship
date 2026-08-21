import numpy as np

from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        loaded = self.vector_store.load()

        if not loaded:

            raise ValueError(
                "Vector database not found. "
                "Run the knowledge base updater first."
            )

    def search(
        self,
        query,
        top_k=3
    ):
        """
        Search the vector database for
        the most relevant chunks.
        """

        query_embedding = (
            self.embedding_model
            .generate_embeddings(
                [query]
            )
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        distances, ids = (
            self.vector_store.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        document_map = {
            item["id"]: item
            for item in self.vector_store.documents
        }

        for distance, vector_id in zip(
            distances[0],
            ids[0]
        ):

            if vector_id == -1:
                continue

            document = document_map.get(
                int(vector_id)
            )

            if document:

                results.append(
                    {
                        "text": document["text"],
                        "source": document["source"],
                        "distance": float(distance)
                    }
                )

        return results