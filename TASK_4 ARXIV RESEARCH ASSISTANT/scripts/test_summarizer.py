from src.paper_search import PaperSearcher
from src.summarizer import PaperSummarizer


def main():

    print("=" * 70)
    print("TESTING RESEARCH PAPER SUMMARIZATION")
    print("=" * 70)

    searcher = PaperSearcher()

    summarizer = PaperSummarizer()

    query = "transformer neural machine translation"

    print("\nSearching for paper...")

    results = searcher.search(
        query=query,
        top_k=1
    )

    if not results:
        print("No paper found.")
        return

    paper = results[0]

    print("\n" + "=" * 70)
    print("SELECTED PAPER")
    print("=" * 70)

    print("Paper ID :", paper["paper_id"])
    print("Title    :", paper["title"])
    print("Category :", paper["categories"])
    print("Year     :", paper["year"])
    print("Score    :", round(paper["score"], 4))

    print("\nGenerating summary...")

    summary = summarizer.summarize(paper)

    print("\n" + "=" * 70)
    print("RESEARCH PAPER SUMMARY")
    print("=" * 70)

    print(summary)

    print("\n" + "=" * 70)
    print("SUMMARIZATION TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()