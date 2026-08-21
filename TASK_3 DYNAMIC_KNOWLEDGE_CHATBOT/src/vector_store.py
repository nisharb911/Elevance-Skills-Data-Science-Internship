import os
import pickle

import faiss
import numpy as np


class VectorStore:

    def __init__(
        self,
        storage_path="vectorstore/faiss_index"
    ):

        self.storage_path = storage_path

        os.makedirs(
            self.storage_path,
            exist_ok=True
        )

        self.index = None

        # Each record contains:
        # id, source, source_hash, text
        self.documents = []

        self.next_id = 0

    def _get_index_path(self):

        return os.path.join(
            self.storage_path,
            "index.faiss"
        )

    def _get_documents_path(self):

        return os.path.join(
            self.storage_path,
            "documents.pkl"
        )

    def create_index(self, dimension):

        base_index = faiss.IndexFlatL2(
            dimension
        )

        self.index = faiss.IndexIDMap2(
            base_index
        )

        print(
            f"FAISS index created with dimension {dimension}."
        )

    def add_documents(
        self,
        embeddings,
        texts,
        source,
        source_hash
    ):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        if self.index is None:

            dimension = embeddings.shape[1]

            self.create_index(
                dimension
            )

        ids = np.arange(
            self.next_id,
            self.next_id + len(texts),
            dtype="int64"
        )

        self.index.add_with_ids(
            embeddings,
            ids
        )

        for vector_id, text in zip(
            ids,
            texts
        ):

            self.documents.append(
                {
                    "id": int(vector_id),
                    "source": str(source),
                    "source_hash": source_hash,
                    "text": text
                }
            )

        self.next_id += len(texts)

        print(
            f"Added {len(texts)} chunks from {source}."
        )

    def remove_source(self, source):

        source = str(source)

        source_ids = [
            item["id"]
            for item in self.documents
            if item["source"] == source
        ]

        if not source_ids:

            print(
                f"No existing chunks found for {source}."
            )

            return

        ids = np.array(
            source_ids,
            dtype="int64"
        )

        self.index.remove_ids(ids)

        self.documents = [
            item
            for item in self.documents
            if item["source"] != source
        ]

        print(
            f"Removed {len(source_ids)} old chunks from {source}."
        )

    def save(self):

        if self.index is None:

            raise ValueError(
                "Vector index does not exist."
            )

        faiss.write_index(
            self.index,
            self._get_index_path()
        )

        with open(
            self._get_documents_path(),
            "wb"
        ) as file:

            pickle.dump(
                self.documents,
                file
            )

        print(
            f"Vector database saved. "
            f"Total vectors: {self.index.ntotal}"
        )

    def load(self):

        index_path = self._get_index_path()

        documents_path = self._get_documents_path()

        if not os.path.exists(
            index_path
        ):

            return False

        if not os.path.exists(
            documents_path
        ):

            return False

        self.index = faiss.read_index(
            index_path
        )

        with open(
            documents_path,
            "rb"
        ) as file:

            self.documents = pickle.load(
                file
            )

        if self.documents:

            self.next_id = (
                max(
                    item["id"]
                    for item in self.documents
                ) + 1
            )

        else:

            self.next_id = 0

        print(
            f"Vector database loaded. "
            f"Total vectors: {self.index.ntotal}"
        )

        return True

    def count(self):

        if self.index is None:

            return 0

        return self.index.ntotal