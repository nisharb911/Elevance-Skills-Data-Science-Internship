from src.response_strategy import get_response_strategy


def test_positive_strategy():
    strategy = get_response_strategy("positive")

    assert "positive" in strategy.lower()
    assert "warm" in strategy.lower()


def test_neutral_strategy():
    strategy = get_response_strategy("neutral")

    assert "neutral" in strategy.lower()
    assert "professional" in strategy.lower()


def test_negative_strategy():
    strategy = get_response_strategy("negative")

    assert "frustrated" in strategy.lower()
    assert "empathy" in strategy.lower()


def test_uncertain_strategy():
    strategy = get_response_strategy("uncertain")

    assert "uncertain" in strategy.lower()
    assert "neutral" in strategy.lower()