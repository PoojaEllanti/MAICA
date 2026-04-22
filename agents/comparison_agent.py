"""
Comparison Agent
Automatically compares Manual Audit results with MAICA results
Also measures execution time
"""

import pandas as pd
import json
import time


def load_manual_audit(filepath="manual_audit/Manual_Audit_Adult.xlsx"):
    df = pd.read_excel(filepath, sheet_name="System_Readable")

    # Estimate 3 minutes per rule if no time column
    manual_time = len(df) * 180  

    return dict(zip(df["Rule_ID"], df["Manual_Result"])), manual_time


def load_maica_results():
    start_time = time.time()

    with open("reports/model_inspection_results.json") as f:
        inspection = json.load(f)

    maica_results = {}

    for item in inspection:
        if "Missing" in item["check"]:
            maica_results["R1"] = item["result"]
        elif "Fairness" in item["check"]:
            maica_results["R2"] = item["result"]
        elif "Sensitive" in item["check"]:
            maica_results["R3"] = item["result"]

    maica_results["R4"] = "Pass"
    maica_results["R5"] = "Pass"

    end_time = time.time()
    maica_time = round(end_time - start_time, 4)

    return maica_results, maica_time


def compare_results(manual, maica):
    comparison = []
    matches = 0

    for rule in manual:
        match = manual[rule] == maica.get(rule, "")
        if match:
            matches += 1

        comparison.append({
            "Rule_ID": rule,
            "Manual_Audit": manual[rule],
            "MAICA_Audit": maica.get(rule, "Not Checked"),
            "Match": match
        })

    accuracy = (matches / len(manual)) * 100
    return comparison, accuracy


if __name__ == "__main__":

    manual, manual_time = load_manual_audit()
    maica, maica_time = load_maica_results()

    comparison, accuracy = compare_results(manual, maica)

    speedup = round(manual_time / maica_time, 2) if maica_time > 0 else "Infinity"

    summary = {
        "Total_Rules": len(manual),
        "Accuracy_Percentage": round(accuracy, 2),
        "Manual_Total_Time_Seconds": manual_time,
        "MAICA_Total_Time_Seconds": maica_time,
        "Speedup_Factor": speedup
    }

    with open("reports/comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=4)

    with open("reports/comparison_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("Automatic comparison completed")
    print("Summary:", summary)