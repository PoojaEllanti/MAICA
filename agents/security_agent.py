"""
Security Agent
Detects sensitive attributes and generates security audit logs
"""

import pandas as pd
import json
import os

# List of sensitive attributes (finance + healthcare)
SENSITIVE_ATTRIBUTES = [
    "age",
    "sex",
    "gender",
    "race",
    "marital-status",
    "medical_condition",
    "disease",
    "diagnosis"
]

def run_security_agent(dataset_path, domain_name):
    df = pd.read_csv(dataset_path)

    detected = []
    for col in df.columns:
        if col.lower() in SENSITIVE_ATTRIBUTES:
            detected.append(col)

    security_report = {
        "dataset": dataset_path,
        "domain": domain_name,
        "sensitive_attributes_detected": detected,
        "count": len(detected),
        "security_status": "Warning" if detected else "Safe",
        "recommendation": (
            "Apply access control and privacy protection"
            if detected else
            "No immediate security risk detected"
        )
    }

    os.makedirs("reports", exist_ok=True)

    output_path = f"reports/{domain_name}_security_report.json"

    with open(output_path, "w") as f:
        json.dump(security_report, f, indent=4)

    print(f"{domain_name} Security audit completed")

if __name__ == "__main__":
    # Generate BOTH reports

    # Healthcare
    run_security_agent("data/heart_disease_uci.csv", "healthcare")

    # Finance
    run_security_agent("data/adult_audit_data.csv", "finance")