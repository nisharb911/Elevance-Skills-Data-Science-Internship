import json


DATA_PATH = "data/processed/cs_papers.jsonl"


def verify_dataset():

    print("=" * 70)
    print("VERIFYING PROCESSED DATASET")
    print("=" * 70)

    count = 0

    with open(DATA_PATH, "r", encoding="utf-8") as file:

        for line in file:

            if not line.strip():
                continue

            record = json.loads(line)

            count += 1

            if count <= 5:

                print("\n" + "-" * 70)

                print(f"ID          : {record['id']}")
                print(f"Title       : {record['title']}")
                print(f"Categories  : {record['matched_categories']}")
                print(f"Date        : {record['update_date']}")

                print(
                    f"Abstract    : "
                    f"{record['abstract'][:300]}..."
                )

    print("\n" + "=" * 70)
    print(f"Total processed papers: {count:,}")
    print("=" * 70)


if __name__ == "__main__":
    verify_dataset()