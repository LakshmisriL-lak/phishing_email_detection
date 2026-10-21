"""Train the phishing email model.

Usage (locally or in Google Colab):
    python train_model.py

Needs phishing_emails.csv (columns: 'Email Text', 'Email Type') in the same folder.
Creates: phishing_model.pkl, tfidf.pkl, confusion_matrix.png
"""
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from features import extract_features

TEXT_COL = "Email Text"
LABEL_COL = "Email Type"

# 1. Load + clean
df = pd.read_csv("phishing_emails.csv")
df = df.dropna(subset=[TEXT_COL, LABEL_COL]).drop_duplicates(subset=[TEXT_COL])
df["text"] = df[TEXT_COL].astype(str)
df["label"] = df[LABEL_COL].apply(lambda v: 1 if "phish" in str(v).lower() else 0)
print(df["label"].value_counts())

# 2. Features
feat = np.log1p(np.array([extract_features(t) for t in df["text"]], dtype=float))
texts = df["text"].str.lower().values
y = df["label"].values

# 3. Split
idx_train, idx_test = train_test_split(
    np.arange(len(df)), test_size=0.2, random_state=42, stratify=y)

# 4. TF-IDF + URL/keyword features
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
Xt_train = tfidf.fit_transform(texts[idx_train])
Xt_test = tfidf.transform(texts[idx_test])
X_train = hstack([Xt_train, csr_matrix(feat[idx_train])]).tocsr()
X_test = hstack([Xt_test, csr_matrix(feat[idx_test])]).tocsr()

# 5. Train
model = LogisticRegression(max_iter=2000, class_weight="balanced")
model.fit(X_train, y[idx_train])

# 6. Evaluate
pred = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y[idx_test], pred) * 100, 2), "%")
print(classification_report(y[idx_test], pred, target_names=["Safe", "Phishing"]))

cm = confusion_matrix(y[idx_test], pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Safe", "Phishing"], yticklabels=["Safe", "Phishing"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")

# 7. Save
joblib.dump(model, "phishing_model.pkl")
joblib.dump(tfidf, "tfidf.pkl")
print("Saved phishing_model.pkl and tfidf.pkl")
