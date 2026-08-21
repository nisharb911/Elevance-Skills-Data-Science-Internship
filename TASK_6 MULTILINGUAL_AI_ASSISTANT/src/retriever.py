import os
import pickle

import faiss
import numpy as np


class MultilingualRetriever:
    """
    FAISS-based semantic retriever.

    The same multilingual embedding space allows queries in
    different languages to retrieve semantically equivalent
    knowledge.
    """

    def __init__(
        self,
        embedder,
        index_path="vectorstore/multilingual.faiss",
        documents_path="vectorstore/documents.pkl",
    ):
        self.embedder = embedder
        self.index_path = index_path
        self.documents_path = documents_path

        self.index = None
        self.documents = []

    def build_index(self, documents):
        if not documents:
            raise ValueError(
                "No documents supplied for indexing."
            )

        self.documents = documents

        texts = [
            document["text"]
            if isinstance(document, dict)
            else str(document)
            for document in documents
        ]

        embeddings = self.embedder.encode(texts)

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

        self.save()

        print(
            f"FAISS index created successfully with "
            f"{len(documents)} documents."
        )

    def search(
        self,
        query,
        top_k=3,
        intent=None
    ):
        """
        Search the FAISS index and optionally rerank
        results using the detected conversational intent.
        """

        if self.index is None:
            self.load()

        if (
            self.index is None
            or self.index.ntotal == 0
        ):
            return []

        query_embedding = self.embedder.encode_single(
            query
        )

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        # Retrieve more candidates initially so that
        # intent-aware reranking has more options.
        candidate_k = min(
            max(top_k * 3, 10),
            self.index.ntotal
        )

        scores, indices = self.index.search(
            query_embedding,
            candidate_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            document = self.documents[index]

            adjusted_score = float(score)

            # ----------------------------------------
            # Intent-aware reranking
            # ----------------------------------------

            if intent:

                category = document[
                    "category"
                ].lower()

                intent_mapping = {

                    "order_status": [
                        "order status",
                        "order tracking",
                    ],

                    "delivery_time": [
                        "delivery",
                        "delivery delay",
                    ],

                    "cancel_order": [
                        "order cancellation",
                    ],

                    "refund": [
                        "refund",
                    ],

                    "return_product": [
                        "product return",
                    ],

                    "change_address": [
                        "address change",
                    ],

                    "payment_issue": [
                        "payment",
                    ],

                    "product_information": [
                        "product information",
                    ],
                }

                relevant_categories = (
                    intent_mapping.get(
                        intent,
                        []
                    )
                )

                if any(
                    item in category
                    for item in relevant_categories
                ):
                    adjusted_score += 0.15

            results.append(
                {
                    "document": document,
                    "score": adjusted_score,
                    "semantic_score": float(score),
                }
            )

        # Highest adjusted score first
        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]

    def save(self):
        os.makedirs(
            os.path.dirname(self.index_path),
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.documents_path,
            "wb"
        ) as file:

            pickle.dump(
                self.documents,
                file
            )

    def load(self):
        if not os.path.exists(
            self.index_path
        ):
            return False

        if not os.path.exists(
            self.documents_path
        ):
            return False

        self.index = faiss.read_index(
            self.index_path
        )

        with open(
            self.documents_path,
            "rb"
        ) as file:

            self.documents = pickle.load(
                file
            )

        return True