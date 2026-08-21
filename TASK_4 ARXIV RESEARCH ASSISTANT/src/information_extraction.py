import re
from collections import Counter


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "are",
    "was",
    "were",
    "have",
    "has",
    "been",
    "using",
    "used",
    "use",
    "into",
    "such",
    "their",
    "these",
    "those",
    "which",
    "than",
    "also",
    "can",
    "may",
    "more",
    "most",
    "other",
    "our",
    "we",
    "they",
    "its",
    "it",
    "an",
    "a",
    "of",
    "to",
    "in",
    "on",
    "is",
    "as",
    "by",
    "or",
    "be",
    "at",
    "through",
    "based",
    "paper",
    "results",
    "approach",
    "method"
}


def tokenize(text: str):
    """
    Convert text into normalized word tokens.
    """

    text = text.lower()

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b",
        text
    )

    return words


def extract_keywords(text: str, top_n: int = 15):
    """
    Extract frequently occurring meaningful terms.
    """

    words = tokenize(text)

    filtered_words = [
        word
        for word in words
        if word not in STOPWORDS
    ]

    counts = Counter(filtered_words)

    return [
        word
        for word, _ in counts.most_common(top_n)
    ]


def extract_technical_terms(text: str):
    """
    Identify potentially technical terms based on
    common research terminology patterns.
    """

    technical_patterns = [
        r"\bCNN\b",
        r"\bRNN\b",
        r"\bLSTM\b",
        r"\bGRU\b",
        r"\bGAN\b",
        r"\bTransformer\b",
        r"\bBERT\b",
        r"\bGPT\b",
        r"\bNLP\b",
        r"\bneural network\b",
        r"\bdeep learning\b",
        r"\bmachine learning\b",
        r"\breinforcement learning\b",
        r"\bcomputer vision\b",
        r"\battention\b",
        r"\bself-attention\b",
        r"\blogistic regression\b",
        r"\bsupport vector machine\b",
        r"\bdecision tree\b",
        r"\brandom forest\b",
        r"\bclustering\b",
        r"\bclassification\b",
        r"\bregression\b",
        r"\bembedding\b",
        r"\bembeddings\b"
    ]

    found_terms = set()

    text_lower = text.lower()

    for pattern in technical_patterns:

        matches = re.findall(
            pattern,
            text_lower,
            flags=re.IGNORECASE
        )

        for match in matches:
            found_terms.add(match.lower())

    return sorted(found_terms)


def extract_information(record: dict):
    """
    Extract useful information from an arXiv paper.
    """

    title = record.get("title", "")
    abstract = record.get("abstract", "")

    full_text = f"{title}. {abstract}"

    keywords = extract_keywords(
        full_text,
        top_n=15
    )

    technical_terms = extract_technical_terms(
        full_text
    )

    return {
        "keywords": keywords,
        "technical_terms": technical_terms
    }