import os
import pandas as pd

DATA_DIR = "data/raw"

print("=" * 60)
print("ARXIV DATASET INSPECTION")
print("=" * 60)

print("\nFiles found:")

for file in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, file)

    if os.path.isfile(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)

        print(f"{file:<40} {size_mb:.2f} MB")

print("\nDataset inspection completed.")