from src.retriever import Retriever


def main():

    print(
        "\n=============================="
    )

    print(
        "RETRIEVER TEST"
    )

    print(
        "==============================\n"
    )

    retriever = Retriever()

    query = (
    "What new synchronization process "
    "was introduced?"
)

    print(
        f"Query: {query}\n"
    )

    results = retriever.search(
        query,
        top_k=3
    )

    if not results:

        print(
            "No relevant documents found."
        )

        return

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {index}"
        )

        print(
            "-" * 40
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Distance: {result['distance']:.4f}"
        )

        print(
            f"Text:\n{result['text']}"
        )


if __name__ == "__main__":

    main()