from src.retriever import ResearchRetriever


def print_results(
    query,
    results
):

    print("\n" + "=" * 70)

    print(
        f"QUERY: {query}"
    )

    print("=" * 70)

    for number, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n[{number}] "
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Paper ID : "
            f"{result['paper_id']}"
        )

        print(
            f"Title    : "
            f"{result['title']}"
        )

        print(
            f"Category : "
            f"{result['categories']}"
        )

        print(
            f"Year     : "
            f"{result['year']}"
        )

        print(
            f"Terms    : "
            f"{result['technical_terms']}"
        )

        print(
            f"Text     : "
            f"{result['text'][:500]}..."
        )


def main():

    print("=" * 70)
    print("RETRIEVER TEST")
    print("=" * 70)

    retriever = ResearchRetriever()

    queries = [

        "How do transformers improve neural machine translation?",

        "What are convolutional neural networks used for?",

        "How is logistic regression used for classification?",

        "What are machine learning techniques for computer vision?"

    ]

    for query in queries:

        results = retriever.search(
            query,
            top_k=5
        )

        print_results(
            query,
            results
        )


if __name__ == "__main__":
    main()