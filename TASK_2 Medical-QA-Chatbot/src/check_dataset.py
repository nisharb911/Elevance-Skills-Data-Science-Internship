from pathlib import Path
import pandas as pd


FILE = Path("data/processed/medical_qa.csv")


if not FILE.exists():

    print("medical_qa.csv was not found.")

    raise SystemExit


df = pd.read_csv(FILE)


print("=" * 60)
print("MedQuAD Processed Dataset Verification")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)


print("\nColumns:")
for column in df.columns:
    print("-", column)


print("\nMissing values:")
print(df.isnull().sum())


print("\nDuplicate rows:")
print(df.duplicated().sum())


print("\nQuestion length statistics:")

question_lengths = df["question"].str.len()

print(question_lengths.describe())


print("\nAnswer length statistics:")

answer_lengths = df["answer"].str.len()

print(answer_lengths.describe())


print("\nQuestion type distribution:")

print(
    df["question_type"]
    .value_counts()
    .head(15)
)


print("\nSource distribution:")

print(
    df["source"]
    .value_counts()
)


print("\nSample records:")

for index, row in df.head(5).iterrows():

    print("\n" + "-" * 60)

    print("Question:")
    print(row["question"])

    print("\nAnswer:")
    print(row["answer"][:500])

    print("\nSource:")
    print(row["source"])