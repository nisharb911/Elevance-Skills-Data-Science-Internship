import json

from src.information_extraction import (
    extract_information
)


DATA_PATH = "data/processed/cs_papers_final.jsonl"


def test_information_extraction():

    print("=" * 70)
    print("TESTING INFORMATION EXTRACTION")
    print("=" * 70)

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        for i, line in enumerate(file):

            if i >= 5:
                break

            record = json.loads(line)

            information = extract_information(
                record
            )

            print("\n" + "-" * 70)

            print(f"Paper ID : {record['id']}")

            print(f"\nTitle:")
            print(record["title"])

            print("\nKeywords:")
            print(
                ", ".join(
                    information["keywords"]
                )
            )

            print("\nTechnical Terms:")

            if information["technical_terms"]:
                print(
                    ", ".join(
                        information["technical_terms"]
                    )
                )
            else:
                print("None detected")


if __name__ == "__main__":
    test_information_extraction()