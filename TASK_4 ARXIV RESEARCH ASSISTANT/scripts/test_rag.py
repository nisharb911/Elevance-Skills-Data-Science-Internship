from src.rag_pipeline import ResearchRAG


def main():

    print("=" * 70)
    print("TESTING COMPLETE RAG PIPELINE")
    print("=" * 70)

    rag = ResearchRAG(top_k=5)

    question = "How do Transformers improve neural machine translation?"

    print("\n")
    print("=" * 70)
    print("USER QUESTION")
    print("=" * 70)
    print(question)

    result = rag.ask(question)

    print("\n")
    print("=" * 70)
    print("GENERATED ANSWER")
    print("=" * 70)

    print(result["answer"])

    print("\n")
    print("=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    for i, source in enumerate(result["sources"], start=1):

        print(f"\n[{i}]")
        print("Paper ID :", source["paper_id"])
        print("Title    :", source["title"])
        print("Category :", source["categories"])
        print("Year     :", source["year"])
        print("Score    :", round(source["score"], 4))


if __name__ == "__main__":
    main()