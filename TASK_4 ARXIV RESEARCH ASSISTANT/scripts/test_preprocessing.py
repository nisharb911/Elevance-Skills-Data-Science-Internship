import json

from src.preprocessing import build_document


DATA_PATH = "data/processed/cs_papers_final.jsonl"


def test_preprocessing():

    print("=" * 70)
    print("TESTING NLP PREPROCESSING")
    print("=" * 70)

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        for i, line in enumerate(file):

            if i >= 3:
                break

            record = json.loads(line)

            document = build_document(record)

            print("\n" + "-" * 70)

            print(f"ID       : {document['id']}")
            print(f"Title    : {document['title']}")
            print(f"Category : {document['matched_categories']}")
            print(f"Year     : {document['year']}")

            print("\nDocument:")
            print(document["text"][:1000])


if __name__ == "__main__":
    test_preprocessing()