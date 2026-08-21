import json
import os

import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INDEX_PATH = "data/vectorstore/research.faiss"
METADATA_PATH = "data/vectorstore/metadata.json"


class ResearchRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            INDEX_PATH
        )

        print("Loading metadata...")

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        print(
            f"Retriever ready: "
            f"{self.index.ntotal:,} vectors"
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        # Convert query into embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Search FAISS
        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            document = self.metadata[index]

            results.append({
                "score": float(score),
                "paper_id": document.get(
                    "paper_id"
                ),
                "title": document.get(
                    "title"
                ),
                "categories": document.get(
                    "categories",
                    []
                ),
                "year": document.get(
                    "year"
                ),
                "keywords": document.get(
                    "keywords",
                    []
                ),
                "technical_terms": document.get(
                    "technical_terms",
                    []
                ),
                "text": document.get(
                    "text",
                    ""
                ),
                "chunk_id": document.get(
                    "chunk_id"
                )
            })

        return results