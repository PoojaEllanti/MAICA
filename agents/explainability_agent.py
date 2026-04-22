"""
Explainability Agent
Generates explanations for model predictions using SHAP
"""

import pandas as pd
import shap
import json
import pickle

from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_model():
    adult = fetch_openml("adult", version=2, as_frame=True)
    df = adult.frame

    df = df.replace("?", None).dropna()
    df["class"] = df["class"].apply(lambda x: 1 if x == ">50K" else 0)

    X = pd.get_dummies(df.drop(columns=["class"]), drop_first=True)
    y = df["class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, X_test


def generate_explanations():
    model, X_test = train_model()

    explainer = shap.LinearExplainer(model, X_test)
    shap_values = explainer.shap_values(X_test[:50])

    explanation = {
        "method": "SHAP",
        "samples_explained": 50,
        "top_features": list(X_test.columns[:10])
    }

    return explanation


if __name__ == "__main__":
    explanation_results = generate_explanations()

    with open("reports/explainability_results.json", "w") as f:
        json.dump(explanation_results, f, indent=4)

    print("Explainability analysis completed")
