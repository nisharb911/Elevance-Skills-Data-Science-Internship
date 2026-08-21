from pathlib import Path

from src.document_loader import load_webpage
from src.text_processor import clean_text, split_text
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.web_source_manager import WebSourceManager


URL_FILE = Path(
    "data/sources/urls.txt"
)


class WebKnowledgeUpdater:

    def __init__(self):

        self.source_manager = (
            WebSourceManager()
        )

        self.embedding_model = (
            EmbeddingModel()
        )

        self.vector_store = (
            VectorStore()
        )

        self.vector_store.load()

    def get_urls(self):

        if not URL_FILE.exists():

            return []

        with open(
            URL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            urls = []

            for line in file:

                url = line.strip()

                if (
                    url
                    and not url.startswith("#")
                ):

                    urls.append(url)

        return urls

    def process_url(
        self,
        url
    ):

        print(
            f"\nChecking URL: {url}"
        )

        try:

            text = load_webpage(
                url
            )

        except Exception as error:

            print(
                f"Failed to download URL: {error}"
            )

            return

        text = clean_text(
            text
        )

        if not text:

            print(
                "No useful text found."
            )

            return

        content_hash = (
            self.source_manager
            .calculate_hash(text)
        )

        status = (
            self.source_manager
            .check_source(
                url,
                content_hash
            )
        )

        print(
            f"Source status: {status.upper()}"
        )

        if status == "unchanged":

            print(
                "No changes detected. Skipping."
            )

            return

        if status == "modified":

            print(
                "Removing old webpage chunks..."
            )

            self.vector_store.remove_source(
                url
            )

        chunks = split_text(
            text,
            chunk_size=500,
            chunk_overlap=50
        )

        if not chunks:

            print(
                "No chunks generated."
            )

            return

        print(
            f"Created {len(chunks)} chunks."
        )

        embeddings = (
            self.embedding_model
            .generate_embeddings(
                chunks
            )
        )

        self.vector_store.add_documents(
            embeddings=embeddings,
            texts=chunks,
            source=url,
            source_hash=content_hash
        )

        self.vector_store.save()

        self.source_manager.update_source(
            url=url,
            content_hash=content_hash,
            chunk_count=len(chunks)
        )

        print(
            "Web source updated successfully."
        )

    def update_all_urls(self):

        urls = self.get_urls()

        if not urls:

            print(
                "No URLs configured."
            )

            return

        print(
            f"Found {len(urls)} configured URLs."
        )

        for url in urls:

            self.process_url(
                url
            )


if __name__ == "__main__":

    updater = WebKnowledgeUpdater()

    updater.update_all_urls()