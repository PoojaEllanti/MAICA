"""
Runtime Monitoring Agent
Simulates continuous monitoring of AI model predictions
"""

import pandas as pd
import json


def load_audit_data(filepath="data/adult_audit_data.csv"):
    return pd.read_csv(filepath)


def monitor_predictions(df):
    # Percentage of positive predictions
    positive_rate = df["predicted"].mean()

    alerts = []

    if positive_rate > 0.7:
        alerts.append({
            "alert": "High Positive Prediction Rate",
            "severity": "Medium",
            "details": f"Positive prediction rate = {positive_rate:.2f}"
        })

    if positive_rate < 0.3:
        alerts.append({
            "alert": "Low Positive Prediction Rate",
            "severity": "Medium",
            "details": f"Positive prediction rate = {positive_rate:.2f}"
        })

    return alerts


def run_monitoring():
    df = load_audit_data()
    alerts = monitor_predictions(df)
    return alerts


if __name__ == "__main__":
    monitoring_results = run_monitoring()

    with open("reports/runtime_monitoring_results.json", "w") as f:
        json.dump(monitoring_results, f, indent=4)

    print("Runtime monitoring completed")
