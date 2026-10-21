"""Flask backend: loads the trained model and serves the website + /api/check."""
import os
import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request
from scipy.sparse import hstack, csr_matrix

from features import extract_features, find_urls, red_flags, advice

BASE = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE, "phishing_model.pkl"))
tfidf = joblib.load(os.path.join(BASE, "tfidf.pkl"))
WORDS = tfidf.get_feature_names_out()

app = Flask(__name__)


def predict(text):
    vec = tfidf.transform([text.lower()])
    extra = csr_matrix(np.log1p(np.array([extract_features(text)], dtype=float)))
    p = model.predict_proba(hstack([vec, extra]).tocsr())[0][1]
    return float(p), vec


def top_words(vec, n=8):
    """Words in this email that pushed the model towards 'Phishing'."""
    contrib = vec.multiply(model.coef_[0][:len(WORDS)]).tocoo()
    ranked = sorted(zip(contrib.col, contrib.data), key=lambda x: x[1], reverse=True)
    return [WORDS[i] for i, s in ranked if s > 0][:n]


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/api/check")
def check():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    if not text:
        return jsonify(error="Please paste an email first."), 400
    text = text[:20000]

    p, vec = predict(text)
    percent = min(max(round(p * 100), 2), 98)
    risk = "HIGH" if p >= 0.7 else "MEDIUM" if p >= 0.4 else "LOW"

    flags = red_flags(text)
    words = top_words(vec)
    if words:
        flags.append("Words the model linked to phishing: " + ", ".join(words))

    return jsonify(
        label="Phishing" if p >= 0.5 else "Safe",
        phishing_percent=percent,
        risk=risk,
        flags=flags,
        advice=advice(risk, text),
        urls=find_urls(text),
    )


if __name__ == "__main__":
    app.run(debug=True)
