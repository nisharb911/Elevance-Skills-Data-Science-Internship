from src.retriever import retrieve_information


def test_payment_retrieval():
    results = retrieve_information(
        "What payment methods do you accept?"
    )

    assert isinstance(results, str)
    assert "## Payments" in results


def test_delivery_retrieval():
    results = retrieve_information(
        "How long does delivery take?"
    )

    assert isinstance(results, str)
    assert "## Order Delivery" in results


def test_refund_retrieval():
    results = retrieve_information(
        "What is the refund policy?"
    )

    assert isinstance(results, str)
    assert "## Refunds" in results