from src.rag_pipeline import ResearchRAG


def print_separator():
    print("=" * 70)


def run_test(rag, question, test_name):
    print_separator()
    print(f"TEST: {test_name}")
    print_separator()

    print(f"\nQuestion:\n{question}")

    result = rag.ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for i, source in enumerate(result["sources"], start=1):
        print(f"\n[{i}]")
        print(f"Paper ID : {source.get('paper_id')}")
        print(f"Title    : {source.get('title')}")
        print(f"Score    : {source.get('score'):.4f}")


def main():

    print_separator()
    print("FINAL RAG QUALITY TEST")
    print_separator()

    rag = ResearchRAG(top_k=5)

    tests = [

        (
            "How do Transformers improve neural machine translation?",
            "Knowledge-based technical question"
        ),

        (
            "What are the main techniques used in convolutional neural networks?",
            "Computer vision question"
        ),

        (
            "What is the role of logistic regression in classification?",
            "Machine learning question"
        ),

        (
            "Tell me about a research paper related to neural machine translation.",
            "Paper discovery question"
        ),

        (
            "What is quantum teleportation using biological neural networks?",
            "Low-confidence / potentially unsupported question"
        ),
    ]

    for question, test_name in tests:
        run_test(rag, question, test_name)

    print("\n")
    print_separator()
    print("FINAL RAG QUALITY TEST COMPLETED")
    print_separator()


if __name__ == "__main__":
    main()