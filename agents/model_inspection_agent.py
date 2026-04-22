"""
Model Inspection Agent
Automatically audits model outputs for data quality, bias, and fairness
"""

import pandas as pd
import json


def load_audit_data(filepath="data/adult_audit_data.csv"):
    return pd.read_csv(filepath)


def load_rules(filepath="reports/regulation_rules.json"):
    with open(filepath, "r") as f:
        return json.load(f)


def inspect_data_quality(df):
    missing = df.isnull().sum().sum()
    return {
        "check": "Missing Values",
        "result": "Pass" if missing == 0 else "Fail",
        "details": f"Missing values count: {missing}"
    }


def inspect_fairness(df):
    # Gender column after one-hot encoding
    gender_cols = [col for col in df.columns if "sex_Male" in col]

    if not gender_cols:
        return {
            "check": "Gender Fairness",
            "result": "Not Applicable",
            "details": "Gender column not found"
        }

    male_col = gender_cols[0]
    male_preds = df[df[male_col] == 1]["predicted"].mean()
    female_preds = df[df[male_col] == 0]["predicted"].mean()

    diff = abs(male_preds - female_preds)

    return {
        "check": "Gender Fairness",
        "result": "Pass" if diff < 0.1 else "Warning",
        "details": f"Prediction difference: {diff:.3f}"
    }


def inspect_bias(df):
    sensitive_features = [col for col in df.columns if "sex_" in col or "race_" in col]

    return {
        "check": "Sensitive Attributes",
        "result": "Warning" if sensitive_features else "Pass",
        "details": f"Sensitive features found: {sensitive_features}"
    }


def run_inspection():
    df = load_audit_data()
    rules = load_rules()

    results = []
    results.append(inspect_data_quality(df))
    results.append(inspect_fairness(df))
    results.append(inspect_bias(df))

    return results


if __name__ == "__main__":
    inspection_results = run_inspection()

    with open("reports/model_inspection_results.json", "w") as f:
        json.dump(inspection_results, f, indent=4)

    print("Model inspection completed")
