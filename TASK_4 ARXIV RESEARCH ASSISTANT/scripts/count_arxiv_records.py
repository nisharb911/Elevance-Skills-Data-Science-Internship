DATA_PATH = "data/raw/arxiv-metadata-oai-snapshot.json"


def count_records(path):

    count = 0

    print("Counting arXiv records...")
    print("This may take some time because the dataset is large.\n")

    with open(path, "r", encoding="utf-8") as file:

        for line in file:
            if line.strip():
                count += 1

                if count % 1_000_000 == 0:
                    print(f"Processed: {count:,} records")

    print("\n" + "=" * 60)
    print(f"Total records: {count:,}")
    print("=" * 60)


if __name__ == "__main__":
    count_records(DATA_PATH)