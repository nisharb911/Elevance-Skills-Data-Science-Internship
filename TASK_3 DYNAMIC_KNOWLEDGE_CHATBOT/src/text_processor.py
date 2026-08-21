def clean_text(text):
    """Clean unnecessary whitespace from extracted text."""

    text = text.replace("\x00", " ")

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def split_text(text, chunk_size=500, chunk_overlap=50):
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum number of characters per chunk.

    chunk_overlap:
        Number of characters shared between consecutive chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - chunk_overlap

    return chunks