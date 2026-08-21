from transformers import pipeline


# =========================================================
# Load sentiment analysis model
# =========================================================

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

print("Loading sentiment model...")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

print("Sentiment model loaded successfully.")


# =========================================================
# Analyze sentiment
# =========================================================

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a customer message.

    Returns
    -------
    dict
        {
            "sentiment": "positive" / "neutral" / "negative",
            "confidence": float
        }
    """

    # -----------------------------------------------------
    # Handle empty input
    # -----------------------------------------------------

    if not text or not text.strip():

        return {
            "sentiment": "neutral",
            "confidence": 0.0
        }


    # -----------------------------------------------------
    # Get model prediction
    # -----------------------------------------------------

    result = sentiment_pipeline(
        text.strip()
    )[0]


    # -----------------------------------------------------
    # Convert model label
    # -----------------------------------------------------

    label = result["label"].lower()

    confidence = float(
        result["score"]
    )


    # -----------------------------------------------------
    # Standardize sentiment labels
    # -----------------------------------------------------

    if "positive" in label:

        sentiment = "positive"

    elif "negative" in label:

        sentiment = "negative"

    elif "neutral" in label:

        sentiment = "neutral"

    else:

        sentiment = "uncertain"


    # -----------------------------------------------------
    # Return structured result
    # -----------------------------------------------------

    return {
        "sentiment": sentiment,
        "confidence": confidence
    }


# =========================================================
# Test the sentiment analyzer
# =========================================================

if __name__ == "__main__":

    test_messages = [

        "I absolutely love your service!",

        "I am extremely disappointed with your service.",

        "What are your customer support hours?",

        "My order has been delayed and I am extremely frustrated.",

        "Can I pay using UPI?"
    ]


    for message in test_messages:

        result = analyze_sentiment(
            message
        )

        print("\nMessage:", message)

        print(
            "Sentiment:",
            result["sentiment"]
        )

        print(
            f"Confidence: "
            f"{result['confidence'] * 100:.2f}%"
        )
