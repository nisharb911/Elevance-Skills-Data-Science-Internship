import json
import os
from collections import Counter


INPUT_PATH = "data/raw/arxiv-metadata-oai-snapshot.json"
OUTPUT_PATH = "data/processed/cs_papers.jsonl"

TARGET_CATEGORIES = {
    "cs.AI",
    "cs.LG",
    "cs.CL",
    "cs.CV",
    "cs.IR",
    "cs.SE",
    "cs.DB",
}

MAX_PAPERS = 20_000


def extract_cs_papers():

    os.makedirs("data/processed", exist_ok=True)

    total_records = 0
    selected_records = 0

    category_counts = Counter()

    print("=" * 70)
    print("ARXIV COMPUTER SCIENCE SUBSET EXTRACTION")
    print("=" * 70)

    print(f"\nTarget categories:")
    for category in sorted(TARGET_CATEGORIES):
        print(f"  - {category}")

    print(f"\nMaximum papers: {MAX_PAPERS:,}")
    print(f"Output: {OUTPUT_PATH}")

    with open(INPUT_PATH, "r", encoding="utf-8") as infile, \
         open(OUTPUT_PATH, "w", encoding="utf-8") as outfile:

        for line in infile:

            if not line.strip():
                continue

            total_records += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            categories = record.get("categories", "").split()

            matched_categories = [
                category
                for category in categories
                if category in TARGET_CATEGORIES
            ]

            if not matched_categories:
                continue

            # Skip records without useful text
            title = record.get("title", "").strip()
            abstract = record.get("abstract", "").strip()

            if not title or not abstract:
                continue

            cleaned_record = {
                "id": record.get("id"),
                "title": " ".join(title.split()),
                "abstract": " ".join(abstract.split()),
                "authors": record.get("authors", ""),
                "categories": categories,
                "matched_categories": matched_categories,
                "update_date": record.get("update_date"),
            }

            outfile.write(
                json.dumps(cleaned_record, ensure_ascii=False) + "\n"
            )

            selected_records += 1

            for category in matched_categories:
                category_counts[category] += 1

            if selected_records % 1_000 == 0:
                print(
                    f"Selected: {selected_records:,} | "
                    f"Scanned: {total_records:,}"
                )

            if selected_records >= MAX_PAPERS:
                print("\nMaximum paper limit reached.")
                break

    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETED")
    print("=" * 70)

    print(f"\nTotal records scanned : {total_records:,}")
    print(f"CS papers selected    : {selected_records:,}")

    print("\nSelected category distribution:")

    for category, count in category_counts.most_common():
        print(f"  {category:<10} {count:,}")

    print(f"\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    extract_cs_papers()