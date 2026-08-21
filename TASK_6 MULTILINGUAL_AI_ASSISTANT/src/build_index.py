import pandas as pd

from src.embeddings import MultilingualEmbedder
from src.retriever import MultilingualRetriever


DATA_PATH = "data/knowledge_base.csv"


def main():
    print("=" * 60)
    print("BUILDING MULTILINGUAL KNOWLEDGE BASE")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    documents = []

    for _, row in df.iterrows():
        documents.append(
            {
                "id": int(row["id"]),
                "category": row["category"],
                "text": row["text"],
            }
        )

    print(f"\nLoaded documents: {len(documents)}")

    embedder = MultilingualEmbedder()

    retriever = MultilingualRetriever(
        embedder=embedder
    )

    retriever.build_index(documents)

    print("\n" + "=" * 60)
    print("INDEX BUILD COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()