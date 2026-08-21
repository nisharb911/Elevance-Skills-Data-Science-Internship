from pathlib import Path
import pickle

import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path(
    "data/processed/medical_qa.csv"
)

MODEL_DIR = Path(
    "models"
)

INDEX_FILE = MODEL_DIR / "medical_qa.index"

METADATA_FILE = MODEL_DIR / "qa_metadata.pkl"


# Sentence Transformer model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("\nLoading processed dataset...")

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(
        DATA_FILE
    )

    print(
        f"Dataset loaded successfully."
    )

    print(
        f"Total records: {len(df)}"
    )

    return df


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model():

    print(
        "\nLoading Sentence Transformer model..."
    )

    print(
        f"Model: {MODEL_NAME}"
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    print(
        "Embedding model loaded successfully."
    )

    return model


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(
    model,
    questions
):

    print(
        "\nGenerating question embeddings..."
    )

    embeddings = model.encode(
        questions,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    print(
        "\nEmbeddings generated."
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    return embeddings.astype(
        "float32"
    )


# ============================================================
# BUILD FAISS INDEX
# ============================================================

def build_faiss_index(
    embeddings
):

    print(
        "\nBuilding FAISS index..."
    )

    dimension = embeddings.shape[1]

    print(
        f"Vector dimension: {dimension}"
    )

    # Inner Product with normalized embeddings
    # is equivalent to cosine similarity.
    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    print(
        f"Vectors added to index: "
        f"{index.ntotal}"
    )

    return index


# ============================================================
# SAVE INDEX
# ============================================================

def save_index(
    index,
    df
):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save FAISS index
    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    # Save metadata
    metadata = {

        "questions": df[
            "question"
        ].tolist(),

        "answers": df[
            "answer"
        ].tolist(),

        "question_ids": df[
            "question_id"
        ].tolist(),

        "focus": df[
            "focus"
        ].tolist(),

        "question_type": df[
            "question_type"
        ].tolist(),

        "synonyms": df[
            "synonyms"
        ].tolist(),

        "source": df[
            "source"
        ].tolist(),

        "source_file": df[
            "source_file"
        ].tolist(),

        "url": df[
            "url"
        ].tolist()
    }

    with open(
        METADATA_FILE,
        "wb"
    ) as file:

        pickle.dump(
            metadata,
            file
        )

    print(
        "\nFiles saved successfully."
    )

    print(
        f"FAISS index: {INDEX_FILE}"
    )

    print(
        f"Metadata: {METADATA_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "MedQuAD Semantic Retrieval Index Builder"
    )

    print("=" * 70)

    # Load dataset
    df = load_dataset()

    # Remove empty questions
    df = df[
        df["question"]
        .fillna("")
        .str.strip()
        != ""
    ]

    df = df.reset_index(
        drop=True
    )

    print(
        f"\nQuestions available for indexing: "
        f"{len(df)}"
    )

    # Load model
    model = load_embedding_model()

    # Generate embeddings
    embeddings = create_embeddings(
        model,
        df["question"].tolist()
    )

    # Build FAISS
    index = build_faiss_index(
        embeddings
    )

    # Save
    save_index(
        index,
        df
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "INDEX BUILD COMPLETED"
    )

    print(
        "=" * 70


    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()