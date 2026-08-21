from pathlib import Path

from src.document_loader import load_document
from src.text_processor import clean_text, split_text
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.source_manager import SourceManager


DOCUMENT_FOLDER = Path(
    "data/sources/documents"
)


class KnowledgeBaseUpdater:

    def __init__(self):

        self.source_manager = SourceManager()

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        self.vector_store.load()

    def process_document(
        self,
        file_path
    ):

        print(
            f"\nChecking source: {file_path}"
        )

        result = (
            self.source_manager
            .check_source(file_path)
        )

        status = result["status"]

        print(
            f"Source status: {status.upper()}"
        )

        # --------------------------------
        # UNCHANGED SOURCE
        # --------------------------------

        if status == "unchanged":

            print(
                "No changes detected. Skipping."
            )

            return

        # --------------------------------
        # NEW OR MODIFIED SOURCE
        # --------------------------------

        if status == "modified":

            print(
                "Removing old version..."
            )

            self.vector_store.remove_source(
                file_path
            )

        print(
            "Processing new/modified document..."
        )

        # Load document
        text = load_document(
            file_path
        )

        # Clean text
        text = clean_text(
            text
        )

        # Create chunks
        chunks = split_text(
            text,
            chunk_size=500,
            chunk_overlap=50
        )

        if not chunks:

            print(
                "No text found. Skipping."
            )

            return

        print(
            f"Created {len(chunks)} chunks."
        )

        # Generate embeddings
        embeddings = (
            self.embedding_model
            .generate_embeddings(
                chunks
            )
        )

        # Add to vector database
        self.vector_store.add_documents(
            embeddings=embeddings,
            texts=chunks,
            source=file_path,
            source_hash=result["hash"]
        )

        # Save vector database
        self.vector_store.save()

        # Update source metadata
        self.source_manager.update_source(
            file_path=file_path,
            file_hash=result["hash"],
            chunk_count=len(chunks)
        )

        print(
            "Knowledge base updated successfully."
        )

    def update_all_sources(self):

        print(
            "\n================================"
        )

        print(
            "DYNAMIC KNOWLEDGE BASE UPDATE"
        )

        print(
            "================================\n"
        )

        files = list(
            DOCUMENT_FOLDER.glob("*.txt")
        )

        files += list(
            DOCUMENT_FOLDER.glob("*.pdf")
        )

        if not files:

            print(
                "No documents found."
            )

            return

        for file_path in files:

            self.process_document(
                file_path
            )

        print(
            "\nKnowledge base update completed."
        )

        print(
            f"Total vectors in database: "
            f"{self.vector_store.count()}"
        )


if __name__ == "__main__":

    updater = KnowledgeBaseUpdater()

    updater.update_all_sources()