import os

from src.document_pipeline import process_dataset


INPUT_PATH = (
    "data/processed/cs_papers_final.jsonl"
)

OUTPUT_PATH = (
    "data/processed/research_chunks.jsonl"
)


def main():

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    print("=" * 70)
    print("BUILDING RESEARCH DOCUMENT CHUNKS")
    print("=" * 70)

    process_dataset(
        INPUT_PATH,
        OUTPUT_PATH
    )

    print("\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()