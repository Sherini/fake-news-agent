
import pickle
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from utils import clean_text

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "news.csv"
MODEL_DIR = BASE_DIR / "models"

# 1. Load CSV
print("Loading dataset...")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"CSV file not found: {DATASET_PATH}\n"
        "Update DATASET_PATH to match your actual CSV filename."
    )

df = pd.read_csv(DATASET_PATH)

print("CSV columns:", df.columns.tolist())
print("Total rows:", len(df))

# 2. Validate column names
# This version expects columns named 'text' and 'label'.
required_columns = {"text", "label"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "Expected columns named 'text' and 'label'. "
        f"Found columns: {df.columns.tolist()}. "
        "Update the column names in train_model.py."
    )

# 3. Remove rows without text or labels
df = df.dropna(subset=["text", "label"]).copy()
df["text"] = df["text"].astype(str).str.strip()
df = df[df["text"] != ""]

print("Rows after cleaning missing values:", len(df))
print("Original label distribution:")
print(df["label"].value_counts())

# 4. Convert labels to numeric classes
# Required mapping: 0 = Fake News, 1 = Real News.
# Supports common text labels and numeric 0/1 labels.
def convert_label(value):
    normalized = str(value).strip().lower()

    if normalized in {"fake", "false", "0"}:
        return 0

    if normalized in {"real", "true", "1"}:
        return 1

    raise ValueError(
        f"Unrecognized label: {value!r}. "
        "Expected fake/real or 0/1 labels."
    )

df["label"] = df["label"].apply(convert_label)

if df["label"].nunique() != 2:
    raise ValueError(
        "The CSV must contain both Fake News and Real News samples."
    )

texts = df["text"].tolist()
labels = df["label"].tolist()

print("Label mapping: 0 = Fake News, 1 = Real News")
print("Class distribution:")
print(pd.Series(labels).value_counts().sort_index())

# 5. Split BEFORE fitting the vectorizer
X_train_text, X_test_text, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# 6. Apply the same preprocessing used by app.py
print("Cleaning text...")

X_train_clean = [clean_text(text) for text in X_train_text]
X_test_clean = [clean_text(text) for text in X_test_text]

# 7. Fit TF-IDF only on training data
print("Fitting TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_clean)
X_test = vectorizer.transform(X_test_clean)

print("Number of features:", X_train.shape[1])

# 8. Train only Logistic Regression
print("Training Logistic Regression...")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 9. Evaluate
print("Evaluating model...")

predictions = model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Fake News", "Real News"],
    zero_division=0
))

print("Confusion matrix (rows = actual, columns = predicted):")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

# 10. Save the model and vectorizer
MODEL_DIR.mkdir(parents=True, exist_ok=True)

with open(MODEL_DIR / "model.pkl", "wb") as f:
    pickle.dump(model, f)

with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nLogistic Regression model and vectorizer saved successfully.")
print("Model path:", MODEL_DIR / "model.pkl")
print("Vectorizer path:", MODEL_DIR / "vectorizer.pkl")
