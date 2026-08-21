from src.sentiment import analyze_sentiment


def test_positive_sentiment():
    result = analyze_sentiment(
        "I am extremely happy with your service!"
    )

    assert result["sentiment"] == "positive"
    assert result["confidence"] > 0.5


def test_negative_sentiment():
    result = analyze_sentiment(
        "I am extremely disappointed with your service."
    )

    assert result["sentiment"] == "negative"
    assert result["confidence"] > 0.5


def test_neutral_sentiment():
    result = analyze_sentiment(
        "What payment methods do you accept?"
    )

    assert result["sentiment"] == "neutral"
    assert result["confidence"] > 0.5