import re


def clean_text(text: str) -> str:
    """
    Clean and normalize academic text.
    """

    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary leading/trailing spaces
    text = text.strip()

    return text


def clean_title(title: str) -> str:
    """
    Clean paper title.
    """

    return clean_text(title)


def clean_abstract(abstract: str) -> str:
    """
    Clean paper abstract.
    """

    return clean_text(abstract)


def build_document(record: dict) -> dict:
    """
    Convert a paper record into a structured document.
    """

    title = clean_title(record.get("title", ""))
    abstract = clean_abstract(record.get("abstract", ""))

    document_text = (
        f"Title: {title}\n\n"
        f"Abstract: {abstract}"
    )

    return {
        "id": record.get("id"),
        "title": title,
        "abstract": abstract,
        "authors": record.get("authors", ""),
        "categories": record.get("categories", []),
        "matched_categories": record.get(
            "matched_categories", []
        ),
        "year": record.get("year"),
        "update_date": record.get("update_date"),
        "text": document_text
    }