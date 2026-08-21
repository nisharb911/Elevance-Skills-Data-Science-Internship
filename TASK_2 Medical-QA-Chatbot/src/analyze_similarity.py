from pathlib import Path

import pandas as pd

from retriever import MedicalRetriever


TEST_FILE = Path(
    "evaluation/out_of_domain.csv"
)


def main():

    print("=" * 70)

    print(
        "Out-of-Domain Similarity Analysis"
    )

    print("=" * 70)

    test_df = pd.read_csv(
        TEST_FILE
    )

    retriever = MedicalRetriever()

    results = []

    for _, row in test_df.iterrows():

        query = row["question"]

        search_results = retriever.search(
            query,
            top_k=5
        )

        if not search_results:

            continue

        best = search_results[0]

        results.append({

            "question": query,

            "best_similarity":
                best["score"],

            "matched_question":
                best["question"],

            "focus":
                best["focus"],

            "source":
                best["source"]
        })

    df = pd.DataFrame(
        results
    )

    print(
        "\nResults:"
    )

    print(
        df.to_string(
            index=False
        )
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "Similarity Statistics"
    )

    print(
        "=" * 70
    )

    print(
        df["best_similarity"].describe()
    )

    output_file = Path(
        "evaluation/out_of_domain_results.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSaved to:"
    )

    print(
        output_file
    )


if __name__ == "__main__":

    main()