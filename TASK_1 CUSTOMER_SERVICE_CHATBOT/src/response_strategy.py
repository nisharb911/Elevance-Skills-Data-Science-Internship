def get_response_strategy(sentiment: str) -> str:
    """
    Return instructions for Gemini based on customer sentiment.
    """

    strategies = {
        "positive": (
            "The customer appears positive. "
            "Respond warmly and professionally. "
            "Acknowledge their positive experience and "
            "maintain a friendly tone."
        ),

        "neutral": (
            "The customer appears neutral. "
            "Respond clearly, professionally, and directly. "
            "Focus on solving the customer's request without "
            "unnecessary emotional language."
        ),

        "negative": (
            "The customer appears frustrated or dissatisfied. "
            "Respond with empathy and patience. "
            "Acknowledge their frustration, apologize when appropriate, "
            "and focus on providing a clear solution or next step."
        ),

        "uncertain": (
            "The customer's sentiment is uncertain. "
            "Use a neutral, professional, and polite tone. "
            "Avoid making assumptions about the customer's emotions."
        )
    }

    return strategies.get(
        sentiment,
        strategies["uncertain"]
    )

if __name__ == "__main__":

    test_sentiments = [
        "positive",
        "neutral",
        "negative",
        "uncertain"
    ]

    for sentiment in test_sentiments:

        print("\nSentiment:", sentiment)
        print("Strategy:")
        print(get_response_strategy(sentiment))