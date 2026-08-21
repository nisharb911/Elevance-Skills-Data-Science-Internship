import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INPUT_PATH = "data/processed/research_chunks.jsonl"

INDEX_DIR = "data/vectorstore"

INDEX_PATH = os.path.join(
    INDEX_DIR,
    "research.faiss"
)

METADATA_PATH = os.path.join(
    INDEX_DIR,
    "metadata.json"
)


class EmbeddingIndex:

    def __init__(self):

        print("=" * 70)
        print("LOADING EMBEDDING MODEL")
        print("=" * 70)

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print(
            f"Embedding dimension: "
            f"{self.model.get_embedding_dimension()}"
        )

    def load_chunks(self):

        print("\nLoading research chunks...")

        chunks = []

        with open(
            INPUT_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if line.strip():

                    chunks.append(
                        json.loads(line)
                    )

        print(
            f"Loaded chunks: {len(chunks):,}"
        )

        return chunks

    def create_embeddings(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print("\nCreating embeddings...")
        print(
            f"Total texts: {len(texts):,}"
        )

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings = embeddings.astype(
            np.float32
        )

        print(
            f"\nEmbedding shape: "
            f"{embeddings.shape}"
        )

        return embeddings

    def build_index(self, embeddings):

        dimension = embeddings.shape[1]

        print("\nBuilding FAISS index...")

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(embeddings)

        print(
            f"FAISS vectors: "
            f"{index.ntotal:,}"
        )

        return index

    def save(self, index, chunks):

        os.makedirs(
            INDEX_DIR,
            exist_ok=True
        )

        print("\nSaving FAISS index...")

        faiss.write_index(
            index,
            INDEX_PATH
        )

        print(
            f"FAISS index saved to:\n"
            f"{INDEX_PATH}"
        )

        print("\nSaving metadata...")

        with open(
            METADATA_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chunks,
                file,
                ensure_ascii=False
            )

        print(
            f"Metadata saved to:\n"
            f"{METADATA_PATH}"
        )


def main():

    builder = EmbeddingIndex()

    chunks = builder.load_chunks()

    embeddings = builder.create_embeddings(
        chunks
    )

    index = builder.build_index(
        embeddings
    )

    builder.save(
        index,
        chunks
    )

    print("\n" + "=" * 70)
    print("EMBEDDING PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()