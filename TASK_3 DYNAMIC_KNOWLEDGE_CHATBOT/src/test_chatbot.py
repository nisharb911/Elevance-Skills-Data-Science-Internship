from src.chatbot import RAGChatbot


def main():

    print(
        "\n=============================="
    )

    print(
        "RAG CHATBOT TEST"
    )

    print(
        "==============================\n"
    )

    chatbot = RAGChatbot()

    question = (
    "What new synchronization process "
    "was introduced?"
)

    print(
        f"Question: {question}\n"
    )

    result = chatbot.ask(
        question
    )

    print(
        "ANSWER:"
    )

    print(
        "-" * 50
    )

    print(
        result["answer"]
    )

    print(
        "\nSOURCES:"
    )

    for source in result["sources"]:

        print(
            f"- {source}"
        )


if __name__ == "__main__":

    main()