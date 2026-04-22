"""
Data Protection Agent
Masks sensitive attributes before sharing or storing data
"""

import pandas as pd
import os

SENSITIVE_COLUMNS = ["age", "sex", "num"]

def protect_data(input_path, output_path):
    df = pd.read_csv(input_path)

    for col in SENSITIVE_COLUMNS:
        if col in df.columns:
            df[col] = "***MASKED***"

    os.makedirs("reports", exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Sensitive data masked and protected file generated")

if __name__ == "__main__":
    protect_data(
        "data/heart_disease_uci.csv",
        "reports/protected_healthcare_data.csv"
    )
