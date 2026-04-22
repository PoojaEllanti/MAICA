"""
Regulation Ingestion Agent
Converts high-level compliance requirements into machine-readable rules
"""

import json

def load_regulations():
    """
    Define compliance rules manually (simulating GDPR / AI Act rules)
    """
    rules = [
        {
            "rule_id": "R1",
            "category": "Data Quality",
            "description": "Dataset must not contain missing values",
            "severity": "High"
        },
        {
            "rule_id": "R2",
            "category": "Fairness",
            "description": "Model predictions should be fair across gender",
            "severity": "High"
        },
        {
            "rule_id": "R3",
            "category": "Bias",
            "description": "Sensitive attributes should not dominate predictions",
            "severity": "Medium"
        },
        {
            "rule_id": "R4",
            "category": "Explainability",
            "description": "Model decisions must be explainable",
            "severity": "Medium"
        },
        {
            "rule_id": "R5",
            "category": "Privacy",
            "description": "No direct personal identifiers should be used",
            "severity": "High"
        }
    ]
    return rules


def save_rules(rules, filepath="reports/regulation_rules.json"):
    """
    Save rules in JSON format so other agents can use them
    """
    with open(filepath, "w") as f:
        json.dump(rules, f, indent=4)
    print("Regulation rules saved successfully")


if __name__ == "__main__":
    rules = load_regulations()
    save_rules(rules)
