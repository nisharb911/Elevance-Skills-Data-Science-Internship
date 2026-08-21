import json
import os


DATA_PATH = "data/raw/arxiv-metadata-oai-snapshot.json"


def inspect_arxiv_file(path, num_records=5):

    print("=" * 70)
    print("ARXIV DATASET INSPECTION")
    print("=" * 70)

    if not os.path.exists(path):
        print(f"\nERROR: File not found: {path}")
        return

    file_size_gb = os.path.getsize(path) / (1024 ** 3)

    print(f"\nFile: {path}")
    print(f"Size: {file_size_gb:.2f} GB")

    print(f"\nReading first {num_records} records...\n")

    with open(path, "r", encoding="utf-8") as file:

        for i in range(num_records):

            line = file.readline()

            if not line:
                break

            record = json.loads(line)

            print("-" * 70)
            print(f"Record {i + 1}")

            print(f"ID          : {record.get('id')}")
            print(f"Title       : {record.get('title')}")
            print(f"Authors     : {record.get('authors')}")
            print(f"Categories  : {record.get('categories')}")
            print(f"Update Date : {record.get('update_date')}")

            abstract = record.get("abstract", "")

            print(f"Abstract    : {abstract[:500]}...")

    print("\n" + "=" * 70)
    print("Inspection completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    inspect_arxiv_file(DATA_PATH)