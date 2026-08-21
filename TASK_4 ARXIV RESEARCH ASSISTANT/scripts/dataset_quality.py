import json
from collections import Counter
from datetime import datetime


DATA_PATH = "data/processed/cs_papers.jsonl"


def analyze_dataset():

    total = 0
    missing_title = 0
    missing_abstract = 0
    duplicate_ids = set()
    seen_ids = set()

    category_counts = Counter()
    year_counts = Counter()

    abstract_lengths = []

    with open(DATA_PATH, "r", encoding="utf-8") as file:

        for line in file:

            if not line.strip():
                continue

            record = json.loads(line)

            total += 1

            # ID quality
            paper_id = record.get("id")

            if paper_id in seen_ids:
                duplicate_ids.add(paper_id)

            seen_ids.add(paper_id)

            # Title quality
            title = record.get("title", "").strip()

            if not title:
                missing_title += 1

            # Abstract quality
            abstract = record.get("abstract", "").strip()

            if not abstract:
                missing_abstract += 1
            else:
                abstract_lengths.append(len(abstract.split()))

            # Categories
            for category in record.get("matched_categories", []):
                category_counts[category] += 1

            # Year
            date_value = record.get("update_date")

            if date_value:

                try:
                    year = datetime.strptime(
                        date_value,
                        "%Y-%m-%d"
                    ).year

                    year_counts[year] += 1

                except ValueError:
                    pass

    print("=" * 70)
    print("DATASET QUALITY REPORT")
    print("=" * 70)

    print(f"\nTotal papers          : {total:,}")
    print(f"Missing titles        : {missing_title:,}")
    print(f"Missing abstracts     : {missing_abstract:,}")
    print(f"Duplicate IDs         : {len(duplicate_ids):,}")

    if abstract_lengths:

        avg_length = sum(abstract_lengths) / len(abstract_lengths)

        print(
            f"Average abstract size : "
            f"{avg_length:.2f} words"
        )

        print(
            f"Shortest abstract     : "
            f"{min(abstract_lengths)} words"
        )

        print(
            f"Longest abstract      : "
            f"{max(abstract_lengths)} words"
        )

    print("\n" + "-" * 70)
    print("CATEGORY DISTRIBUTION")
    print("-" * 70)

    for category, count in category_counts.most_common():
        print(f"{category:<10} {count:,}")

    print("\n" + "-" * 70)
    print("YEAR DISTRIBUTION")
    print("-" * 70)

    for year, count in sorted(year_counts.items()):
        print(f"{year}: {count:,}")

    print("\n" + "=" * 70)
    print("QUALITY ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    analyze_dataset()