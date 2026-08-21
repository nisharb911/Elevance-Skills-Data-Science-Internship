from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def load_text_file(file_path):
    """Load text from a TXT file."""

    path = Path(file_path)

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def load_pdf_file(file_path):
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


def load_webpage(url):
    """Download and extract readable text from a webpage."""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove elements that usually don't contain
    # useful article information.

    for element in soup(
        ["script", "style", "noscript"]
    ):

        element.decompose()

    text = soup.get_text(
        separator="\n"
    )

    return text


def load_document(file_path):
    """Load TXT or PDF document."""

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".txt":

        return load_text_file(
            file_path
        )

    elif extension == ".pdf":

        return load_pdf_file(
            file_path
        )

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )