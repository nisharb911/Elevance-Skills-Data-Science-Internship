from pathlib import Path

import pandas as pd

from retriever import MedicalRetriever


# ============================================================
# CONFIGURATION
# ============================================================

TEST_FILE = Path(
    "evaluation/test_questions.csv"
)

TOP_K = 5


# ============================================================
# CHECK WHETHER RESULT IS RELEVANT
# ============================================================

def is_relevant(result, expected_keywords):
    """
    Basic relevance check.

    A result is considered relevant when the expected
    keywords are found in the retrieved question or answer.
    """

    text = (
        result["question"]
        + " "
        + result["answer"]
    ).lower()

    keywords = [
        keyword.strip().lower()
        for keyword in expected_keywords.split()
        if keyword.strip()
    ]

    if not keywords:
        return False

    matches = sum(
        keyword in text
        for keyword in keywords
    )

    # Require at least half of the expected keywords
    required_matches = max(
        1,
        len(keywords) // 2
    )

    return matches >= required_matches


# ============================================================
# FIND RELEVANT RANK
# ============================================================

def find_relevant_rank(
    results,
    expected_keywords
):

    for rank, result in enumerate(
        results,
        start=1
    ):

        if is_relevant(
            result,
            expected_keywords
        ):

            return rank

    return None


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print("=" * 70)

    print(
        "MedQuAD Retrieval Evaluation"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Load evaluation dataset
    # --------------------------------------------------------

    if not TEST_FILE.exists():

        raise FileNotFoundError(
            f"Evaluation file not found: "
            f"{TEST_FILE}"
        )

    test_df = pd.read_csv(
        TEST_FILE
    )

    print(
        f"\nEvaluation questions: "
        f"{len(test_df)}"
    )

    # --------------------------------------------------------
    # Load retriever
    # --------------------------------------------------------

    retriever = MedicalRetriever()

    # --------------------------------------------------------
    # Evaluation counters
    # --------------------------------------------------------

    top1_correct = 0

    top3_correct = 0

    top5_correct = 0

    reciprocal_ranks = []

    detailed_results = []

    # --------------------------------------------------------
    # Evaluate each question
    # --------------------------------------------------------

    for index, row in test_df.iterrows():

        question = row["question"]

        expected_keywords = row[
            "expected_keywords"
        ]

        results = retriever.search(
            question,
            top_k=TOP_K
        )

        relevant_rank = find_relevant_rank(
            results,
            expected_keywords
        )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        if relevant_rank == 1:

            top1_correct += 1

        if (
            relevant_rank is not None
            and relevant_rank <= 3
        ):

            top3_correct += 1

        if (
            relevant_rank is not None
            and relevant_rank <= 5
        ):

            top5_correct += 1

        # ----------------------------------------------------
        # MRR
        # ----------------------------------------------------

        if relevant_rank is not None:

            reciprocal_rank = (
                1 / relevant_rank
            )

        else:

            reciprocal_rank = 0

        reciprocal_ranks.append(
            reciprocal_rank
        )

        # ----------------------------------------------------
        # Store detailed result
        # ----------------------------------------------------

        best_score = (
            results[0]["score"]
            if results
            else 0
        )

        detailed_results.append({

            "question": question,

            "relevant_rank":
                relevant_rank,

            "best_similarity":
                best_score
        })

        # ----------------------------------------------------
        # Print result
        # ----------------------------------------------------

        print(
            "\n" + "-" * 70
        )

        print(
            f"Question {index + 1}: "
            f"{question}"
        )

        if relevant_rank is not None:

            print(
                f"Relevant result rank: "
                f"{relevant_rank}"
            )

        else:

            print(
                "Relevant result: Not found "
                "in Top-5"
            )

        print(
            f"Best similarity: "
            f"{best_score:.4f}"
        )

        if results:

            print(
                f"Top result: "
                f"{results[0]['question']}"
            )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    total = len(test_df)

    top1_accuracy = (
        top1_correct / total
    )

    top3_accuracy = (
        top3_correct / total
    )

    top5_accuracy = (
        top5_correct / total
    )

    mrr = sum(
        reciprocal_ranks
    ) / total

    # --------------------------------------------------------
    # Print final results
    # --------------------------------------------------------

    print(
        "\n\n" + "=" * 70
    )

    print(
        "RETRIEVAL EVALUATION RESULTS"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTotal test questions: "
        f"{total}"
    )

    print(
        f"\nTop-1 Accuracy: "
        f"{top1_accuracy:.2%}"
    )

    print(
        f"Top-3 Accuracy: "
        f"{top3_accuracy:.2%}"
    )

    print(
        f"Top-5 Accuracy: "
        f"{top5_accuracy:.2%}"
    )

    print(
        f"Mean Reciprocal Rank (MRR): "
        f"{mrr:.4f}"
    )

    # --------------------------------------------------------
    # Save detailed results
    # --------------------------------------------------------

    results_df = pd.DataFrame(
        detailed_results
    )

    output_file = Path(
        "evaluation/retrieval_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nDetailed results saved to:"
    )

    print(
        output_file
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()