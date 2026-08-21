from src.llm_generator import ResearchLLM


def main():

    print("=" * 70)
    print("TESTING OPEN-SOURCE LLM")
    print("=" * 70)

    llm = ResearchLLM()

    context = """
    Paper: Attention Is All You Need

    The Transformer is a neural network architecture based entirely
    on attention mechanisms. Unlike recurrent neural networks,
    Transformers do not require sequential processing of input tokens.
    This allows greater parallelization during training and helps
    model long-range dependencies.
    """

    question = "Explain why Transformers are useful for neural machine translation."

    answer = llm.generate_answer(
        question=question,
        context=context
    )

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\n" + "=" * 70)
    print("LLM TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()