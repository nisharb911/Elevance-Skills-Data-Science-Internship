from pathlib import Path

from document_loader import load_document
from text_processor import clean_text, split_text
from embeddings import EmbeddingModel
from vector_store import VectorStore


DOCUMENT_PATH = (
    "data/sources/documents/company_information.txt"
)


def main():

    print("\n==============================")
    print("DYNAMIC KNOWLEDGE PIPELINE")
    print("==============================\n")

    # Step 1: Load document
    print("1. Loading document...")

    text = load_document(DOCUMENT_PATH)

    print(
        f"Document loaded. Characters: {len(text)}"
    )

    # Step 2: Clean text
    print("\n2. Cleaning text...")

    text = clean_text(text)

    print(
        f"Cleaned text characters: {len(text)}"
    )

    # Step 3: Split into chunks
    print("\n3. Creating chunks...")

    chunks = split_text(
        text,
        chunk_size=500,
        chunk_overlap=50
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    # Step 4: Generate embeddings
    print("\n4. Generating embeddings...")

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.generate_embeddings(
        chunks
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # Step 5: Create vector database
    print("\n5. Creating FAISS vector database...")

    vector_store = VectorStore()

    vector_store.create_index(
        embeddings
    )

    vector_store.add_documents(
        chunks
    )

    vector_store.save()

    print("\n==============================")
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("==============================\n")


if __name__ == "__main__":
    main()