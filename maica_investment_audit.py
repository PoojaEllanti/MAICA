import json
import os

from investment_app.portfolio_model import generate_portfolio
from investment_app.risk_profiler import determine_risk

from agents.coordinator_agent import generate_final_report


def run_investment_audit():

    print("\nRunning MAICA audit for AI Investment Advisor...\n")

    age = 30
    income = 1500000
    investment = 40000
    risk = "Medium"

    risk_level = determine_risk(age, income, risk)

    portfolio, strategy = generate_portfolio(risk_level, investment)

    print("Generated Portfolio:\n")
    print(json.dumps(portfolio, indent=4))

    print("\nRunning MAICA compliance agents...\n")

    report = generate_final_report("finance")

    os.makedirs("reports", exist_ok=True)

    report_path = "reports/investment_compliance_report.json"

    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print("\nCompliance Report Generated:")
    print(report_path)

    print("\nAudit Summary:")

    print(report["summary"])


if __name__ == "__main__":
    run_investment_audit()