import pickle
import numpy as np
import shap
from lime.lime_text import LimeTextExplainer

# -------------------------------
# Load Model & Vectorizer
# -------------------------------
model = pickle.load(open("models/model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
x_train_text = pickle.load(open("models/x_train_text.pkl", "rb"))

# -------------------------------
# SHAP Explainer
# -------------------------------
explainer = shap.Explainer(
    model,
    vectorizer.transform(x_train_text)
)

# -------------------------------
# LIME Explainer
# -------------------------------
lime_explainer = LimeTextExplainer(
    class_names=["Fake News", "Real News"]
)


def predict_proba(texts):
    """
    Required by LIME.
    Converts text into TF-IDF and returns probabilities.
    """
    vectors = vectorizer.transform(texts)
    return model.predict_proba(vectors)


# ===================================================
# SHAP
# ===================================================

def shap_explanation(text, top_n=10):

    cleaned = text.lower()

    vector = vectorizer.transform([cleaned])

    shap_values = explainer(vector)

    feature_names = vectorizer.get_feature_names_out()

    values = shap_values.values[0]

    important = np.argsort(np.abs(values))[::-1]

    words = []

    for idx in important[:top_n]:

        if values[idx] != 0:

            words.append({

                "word": feature_names[idx],

                "impact": round(float(values[idx]), 4)

            })

    return words


# ===================================================
# LIME
# ===================================================

def lime_explanation(text, top_n=10):

    explanation = lime_explainer.explain_instance(
        text,
        predict_proba,
        num_features=top_n
    )

    words = []

    for feature, weight in explanation.as_list():

        words.append({

            "word": feature,

            "impact": round(weight, 4)

        })

    return words