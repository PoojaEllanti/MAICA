"""
Coordinator Agent
Aggregates results from all MAICA agents into a final compliance report
"""

import json
import os

def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_final_report(domain_name):
    report = {
        "domain": domain_name,
        "regulation_rules": load_json("reports/regulation_rules.json"),
        "model_inspection": load_json("reports/model_inspection_results.json"),
        "runtime_monitoring": load_json("reports/runtime_monitoring_results.json"),
        "explainability": load_json("reports/explainability_results.json"),
        "summary": {
            "overall_compliance": "Partially Compliant",
            "notes": f"Automated auditing results for {domain_name} dataset."
        }
    }
    return report


if __name__ == "__main__":

    os.makedirs("reports", exist_ok=True)

    # Generate Healthcare Compliance Report
    healthcare_report = generate_final_report("healthcare")

    with open("reports/healthcare_compliance_report.json", "w") as f:
        json.dump(healthcare_report, f, indent=4)

    print("Healthcare compliance report generated")


    # Generate Finance Compliance Report
    finance_report = generate_final_report("finance")

    with open("reports/finance_compliance_report.json", "w") as f:
        json.dump(finance_report, f, indent=4)

    print("Finance compliance report generated")