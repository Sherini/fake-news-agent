
import os
import pickle
from pathlib import Path

from flask import Flask, jsonify, request

from utils import clean_text
from url_utils import extract_text_from_url

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

app = Flask(__name__)

# Load the existing Logistic Regression model and TF-IDF vectorizer.
with open(MODEL_DIR / "model.pkl", "rb") as f:
    ml_model = pickle.load(f)

with open(MODEL_DIR / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


@app.get("/health")
def health():
    return jsonify({
        "status": "UP",
        "mlModelLoaded": ml_model is not None
    })


def run_prediction(text, want_explanations=True):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    predicted = int(ml_model.predict(vector)[0])
    probabilities = ml_model.predict_proba(vector)[0]
    classes = list(ml_model.classes_)

    # Correctly match the prediction to its probability.
    confidence = float(probabilities[classes.index(predicted)])
    result = "Real News" if predicted == 1 else "Fake News"

    shap_result = []
    lime_result = []

    if want_explanations:
        try:
            from xai import shap_explanation, lime_explanation

            shap_result = shap_explanation(cleaned)
            lime_result = lime_explanation(cleaned)

        except Exception as exc:
            app.logger.warning(
                "SHAP/LIME explanations unavailable: %s", exc
            )

    return result, confidence, shap_result, lime_result


@app.post("/api/predict")
def predict():
    data = request.get_json(silent=True) or {}

    text = (data.get("text") or "").strip()
    url = (data.get("url") or "").strip()
    want_explanations = data.get("explain", True)

    if not isinstance(want_explanations, bool):
        return jsonify({
            "error": "'explain' must be true or false."
        }), 400

    if url:
        extracted = extract_text_from_url(url)

        if not extracted or not extracted.strip():
            return jsonify({
                "error": "Could not extract article text from the URL."
            }), 422

        text = extracted.strip()

    if not text:
        return jsonify({
            "error": "Provide article text or a URL."
        }), 400

    if len(text) > 100000:
        return jsonify({
            "error": "Article is too long; limit is 100,000 characters."
        }), 413

    try:
        result, confidence, shap_result, lime_result = run_prediction(
            text, want_explanations
        )

        return jsonify({
            "prediction": result,
            "confidencePercent": round(confidence * 100, 2),
            "model": "Logistic Regression",
            "shap": shap_result,
            "lime": lime_result,
            "disclaimer": (
                "This is a model prediction, not independent "
                "verification of a news claim."
            )
        })

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Prediction failed. Check the AI service logs."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False
    )
