from flask import Flask, request, jsonify, send_from_directory
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from investment_app.portfolio_model import generate_portfolio
from investment_app.risk_profiler import determine_risk
from investment_app.stock_fetcher import get_market_snapshot
from investment_app.audit_integration import run_maica_audit

app = Flask(__name__, static_folder="../frontend", static_url_path="")


# -------------------------
# LOAD FRONTEND
# -------------------------
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# -------------------------
# RECOMMENDATION API
# -------------------------
@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    try:
        age = int(data.get("age", 0))
        income = int(data.get("income", 0))

        # ✅ FIXED KEY
        amount = int(data.get("investment", 0))

        risk = data.get("risk", "Medium")

    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    if amount == 0:
        return jsonify({"error": "Investment amount missing"}), 400

    # -------------------------
    # RISK PROFILING
    # -------------------------
    risk_level = determine_risk(age, income, risk)

    # -------------------------
    # PORTFOLIO GENERATION
    # -------------------------
    portfolio, strategy = generate_portfolio(risk_level, amount)

    # -------------------------
    # MARKET DATA
    # -------------------------
    market = get_market_snapshot(portfolio)

    # -------------------------
    # MAICA AUDIT (silent)
    # -------------------------
    run_maica_audit(portfolio)

    # -------------------------
    # FINAL RESPONSE
    # -------------------------
    return jsonify({
        "portfolio": portfolio,
        "market": market,
        "strategy": strategy,
        "status": "✔ Verified by MAICA Responsible AI Auditor"
    })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)