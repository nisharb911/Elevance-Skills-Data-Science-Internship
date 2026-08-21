import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from .sentiment import analyze_sentiment


# ---------------------------------------------------------
# Load test dataset
# ---------------------------------------------------------

DATA_PATH = "data/sentiment_test.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully.")
print("Number of test messages:", len(df))


# ---------------------------------------------------------
# Generate predictions
# ---------------------------------------------------------

predictions = []

for text in df["text"]:

    result = analyze_sentiment(text)

    predictions.append(result["sentiment"])


df["predicted_sentiment"] = predictions


# ---------------------------------------------------------
# Calculate accuracy
# ---------------------------------------------------------

accuracy = accuracy_score(
    df["actual_sentiment"],
    df["predicted_sentiment"]
)

print("\nAccuracy:")
print(f"{accuracy * 100:.2f}%")


# ---------------------------------------------------------
# Classification report
# ---------------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        df["actual_sentiment"],
        df["predicted_sentiment"],
        labels=["positive", "neutral", "negative"],
        zero_division=0
    )
)


# ---------------------------------------------------------
# Confusion Matrix
# ---------------------------------------------------------

matrix = confusion_matrix(
    df["actual_sentiment"],
    df["predicted_sentiment"],
    labels=["positive", "neutral", "negative"]
)

print("\nConfusion Matrix:")
print(matrix)