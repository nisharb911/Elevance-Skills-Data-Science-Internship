import json
import os
import random
from collections import Counter


INPUT_PATH = "data/raw/arxiv-metadata-oai-snapshot.json"
OUTPUT_PATH = "data/processed/cs_papers_final.jsonl"


TARGET_CATEGORIES = {
    "cs.AI",
    "cs.LG",
    "cs.CL",
    "cs.CV",
    "cs.IR",
    "cs.SE",
    "cs.DB",
}


TOTAL_TARGET = 20_000

# Target distribution by publication year
TARGET_COUNTS = {
    "recent": 12_000,       # 2018-2026
    "mid": 5_000,           # 2013-2017
    "foundational": 3_000  # 2007-2012
}


def get_period(year):

    if year >= 2018:
        return "recent"

    elif year >= 2013:
        return "mid"

    else:
        return "foundational"


def build_dataset():

    os.makedirs("data/processed", exist_ok=True)

    selected = {
        "recent": [],
        "mid": [],
        "foundational": []
    }

    seen_ids = set()

    total_scanned = 0
    valid_cs_records = 0

    print("=" * 70)
    print("BUILDING BALANCED ARXIV CS DATASET")
    print("=" * 70)

    print("\nTarget categories:")

    for category in sorted(TARGET_CATEGORIES):
        print(f"  - {category}")

    print("\nTarget distribution:")

    for period, count in TARGET_COUNTS.items():
        print(f"  {period:<15}: {count:,}")

    print("\nScanning full arXiv dataset...\n")

    with open(INPUT_PATH, "r", encoding="utf-8") as infile:

        for line in infile:

            if not line.strip():
                continue

            total_scanned += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            paper_id = record.get("id")

            if not paper_id or paper_id in seen_ids:
                continue

            categories = record.get("categories", "").split()

            matched_categories = [
                category
                for category in categories
                if category in TARGET_CATEGORIES
            ]

            if not matched_categories:
                continue

            title = record.get("title", "").strip()
            abstract = record.get("abstract", "").strip()
            update_date = record.get("update_date")

            if not title or not abstract or not update_date:
                continue

            try:
                year = int(update_date[:4])
            except ValueError:
                continue

            period = get_period(year)

            if len(selected[period]) >= TARGET_COUNTS[period]:
                continue

            cleaned_record = {
                "id": paper_id,
                "title": " ".join(title.split()),
                "abstract": " ".join(abstract.split()),
                "authors": record.get("authors", ""),
                "categories": categories,
                "matched_categories": matched_categories,
                "update_date": update_date,
                "year": year,
                "period": period
            }

            selected[period].append(cleaned_record)
            seen_ids.add(paper_id)

            valid_cs_records += 1

            if total_scanned % 500_000 == 0:

                print(
                    f"Scanned: {total_scanned:,} | "
                    f"Recent: {len(selected['recent']):,} | "
                    f"Mid: {len(selected['mid']):,} | "
                    f"Foundational: {len(selected['foundational']):,}"
                )

            if all(
                len(selected[p]) >= TARGET_COUNTS[p]
                for p in TARGET_COUNTS
            ):
                print("\nAll targets reached.")
                break

    # Combine datasets
    final_records = (
        selected["recent"]
        + selected["mid"]
        + selected["foundational"]
    )

    # Shuffle records
    random.seed(42)
    random.shuffle(final_records)

    # Save JSONL
    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as outfile:

        for record in final_records:

            outfile.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    # Category statistics
    category_counts = Counter()

    for record in final_records:

        for category in record["matched_categories"]:
            category_counts[category] += 1

    print("\n" + "=" * 70)
    print("FINAL DATASET CREATED")
    print("=" * 70)

    print(f"\nTotal records scanned : {total_scanned:,}")
    print(f"Final papers          : {len(final_records):,}")

    print("\nPeriod distribution:")

    for period in TARGET_COUNTS:
        count = sum(
            1 for r in final_records
            if r["period"] == period
        )

        print(f"  {period:<15}: {count:,}")

    print("\nCategory distribution:")

    for category, count in category_counts.most_common():
        print(f"  {category:<10} {count:,}")

    print("\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_dataset()