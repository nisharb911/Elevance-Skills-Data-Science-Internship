import json
from collections import Counter


DATA_PATH = "data/raw/arxiv-metadata-oai-snapshot.json"


def analyze_categories(path):

    category_counter = Counter()

    print("Analyzing arXiv categories...")
    print("This will scan the dataset line by line.\n")

    with open(path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            record = json.loads(line)

            categories = record.get("categories", "")

            for category in categories.split():
                category_counter[category] += 1

            if line_number % 1_000_000 == 0:
                print(f"Processed: {line_number:,} records")

    print("\n" + "=" * 70)
    print("TOP ARXIV CATEGORIES")
    print("=" * 70)

    for category, count in category_counter.most_common(30):
        print(f"{category:<15} {count:,}")

    print("\n" + "=" * 70)
    print("Computer Science categories found:")
    print("=" * 70)

    cs_categories = {
        category: count
        for category, count in category_counter.items()
        if category.startswith("cs.")
    }

    for category, count in sorted(
        cs_categories.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{category:<15} {count:,}")


if __name__ == "__main__":
    analyze_categories(DATA_PATH)