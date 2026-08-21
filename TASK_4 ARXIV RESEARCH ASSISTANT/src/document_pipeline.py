import json

from src.preprocessing import build_document
from src.information_extraction import extract_information
from src.chunking import create_chunks


def process_record(record: dict):
    """
    Complete processing pipeline for one paper.
    """

    document = build_document(record)

    information = extract_information(
        record
    )

    document["keywords"] = information[
        "keywords"
    ]

    document["technical_terms"] = information[
        "technical_terms"
    ]

    chunks = create_chunks(document)

    return chunks


def process_dataset(
    input_path: str,
    output_path: str
):

    total_papers = 0
    total_chunks = 0

    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as infile, open(
        output_path,
        "w",
        encoding="utf-8"
    ) as outfile:

        for line in infile:

            if not line.strip():
                continue

            record = json.loads(line)

            chunks = process_record(record)

            for chunk in chunks:

                outfile.write(
                    json.dumps(
                        chunk,
                        ensure_ascii=False
                    ) + "\n"
                )

                total_chunks += 1

            total_papers += 1

            if total_papers % 1000 == 0:

                print(
                    f"Processed papers: "
                    f"{total_papers:,} | "
                    f"Chunks: "
                    f"{total_chunks:,}"
                )

    print("\n" + "=" * 70)
    print("DOCUMENT PROCESSING COMPLETED")
    print("=" * 70)

    print(
        f"Total papers : {total_papers:,}"
    )

    print(
        f"Total chunks : {total_chunks:,}"
    )