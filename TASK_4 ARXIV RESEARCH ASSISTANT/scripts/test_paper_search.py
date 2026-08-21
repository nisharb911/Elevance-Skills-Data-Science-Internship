from src.paper_search import PaperSearcher


def main():

    print("=" * 70)
    print("TESTING RESEARCH PAPER SEARCH")
    print("=" * 70)

    searcher = PaperSearcher()

    queries = [
        "transformer neural machine translation",
        "convolutional neural networks computer vision",
        "machine learning classification"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        results = searcher.search(
            query=query,
            top_k=5
        )

        for i, result in enumerate(results, start=1):

            print(f"\n[{i}]")
            print("Paper ID :", result["paper_id"])
            print("Title    :", result["title"])
            print("Category :", result["categories"])
            print("Year     :", result["year"])
            print("Score    :", round(result["score"], 4))


if __name__ == "__main__":
    main()