from src.embeddings import MultilingualEmbedder
from src.retriever import MultilingualRetriever


def main():
    print("=" * 60)
    print("CROSS-LINGUAL RETRIEVAL TEST")
    print("=" * 60)

    embedder = MultilingualEmbedder()

    retriever = MultilingualRetriever(
        embedder=embedder
    )

    if not retriever.load():
        print("FAISS index not found.")
        print("Run: python -m src.build_index")
        return

    queries = [
        ("English", "Where is my order?"),
        ("Hindi", "मेरा ऑर्डर कहाँ है?"),
        ("Marathi", "माझी ऑर्डर कुठे आहे?"),
        ("Gujarati", "મારું ઓર્ડર ક્યાં છે?"),
    ]

    for language, query in queries:
        print("\n" + "-" * 60)
        print(f"Language: {language}")
        print(f"Query: {query}")

        results = retriever.search(
            query,
            top_k=2
        )

        for result in results:
            document = result["document"]
            score = result["score"]

            print(
                f"\nScore: {score:.4f}"
            )

            print(
                f"Category: {document['category']}"
            )

            print(
                f"Knowledge: {document['text']}"
            )


if __name__ == "__main__":
    main()