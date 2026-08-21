from langchain_text_splitters import RecursiveCharacterTextSplitter


# Character-based chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def create_chunks(document: dict):
    """
    Split a research document into overlapping chunks
    while preserving paper metadata.
    """

    text = document.get("text", "")

    if not text:
        return []

    chunks = text_splitter.split_text(text)

    results = []

    for index, chunk in enumerate(chunks):

        results.append({
            "chunk_id": f"{document['id']}_chunk_{index}",
            "paper_id": document["id"],
            "chunk_index": index,
            "title": document["title"],
            "categories": document.get(
                "categories", []
            ),
            "matched_categories": document.get(
                "matched_categories", []
            ),
            "year": document.get("year"),
            "update_date": document.get(
                "update_date"
            ),
            "keywords": document.get(
                "keywords", []
            ),
            "technical_terms": document.get(
                "technical_terms", []
            ),
            "text": chunk
        })

    return results