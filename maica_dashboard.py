import streamlit as st
import pandas as pd
import plotly.express as px

from investment_app.portfolio_model import generate_portfolio
from investment_app.risk_profiler import determine_risk
from agents.coordinator_agent import generate_final_report

st.set_page_config(
    page_title="MAICA Portfolio Audit Dashboard",
    layout="wide"
)

# ------------------------------
# TITLE
# ------------------------------
st.title("MAICA Responsible AI Portfolio Dashboard")

st.markdown(
"""
This dashboard evaluates whether the **AI-generated investment portfolio**
follows **Responsible AI principles** such as diversification, fairness,
transparency and explainability.
"""
)

st.divider()

# ------------------------------
# USER INPUT
# ------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    age = st.number_input("Age", value=30)

with col2:
    income = st.number_input("Annual Income", value=1500000)

with col3:
    investment = st.number_input("Investment Amount", value=40000)

with col4:
    risk = st.selectbox("Risk Level", ["Low", "Medium", "High"])

# ------------------------------
# GENERATE PORTFOLIO
# ------------------------------
risk_level = determine_risk(age, income, risk)
portfolio, strategy = generate_portfolio(risk_level, investment)

st.divider()

# ------------------------------
# PORTFOLIO DISPLAY
# ------------------------------
st.subheader("AI Generated Investment Portfolio")

for stock, amount in portfolio.items():
    st.write(f"**{stock}** — ₹{amount}")

# ------------------------------
# PIE CHART
# ------------------------------
st.subheader("Portfolio Distribution")

df = pd.DataFrame({
    "Stock": list(portfolio.keys()),
    "Investment": list(portfolio.values())
})

fig = px.pie(df, names="Stock", values="Investment", title="Allocation")
st.plotly_chart(fig, width="stretch")

# ------------------------------
# STRATEGY
# ------------------------------
st.subheader("Investment Strategy")
st.info(strategy)

# ------------------------------
# RUN MAICA
# ------------------------------
report = generate_final_report("finance")

# ------------------------------
# SCORE
# ------------------------------
def compute_score(report):

    score = 100

    for check in report["model_inspection"]:
        if check["result"] == "Warning":
            score -= 10
        if check["result"] == "Fail":
            score -= 20

    score -= len(report["runtime_monitoring"]) * 5

    return max(score, 0)

score = compute_score(report)

# ------------------------------
# SCORE DISPLAY
# ------------------------------
st.subheader("MAICA Compliance Score")

col1, col2 = st.columns(2)

with col1:
    st.metric("Score", f"{score}%")

with col2:
    if score >= 85:
        st.success("Low Risk Portfolio")
    elif score >= 60:
        st.warning("Moderate Risk")
    else:
        st.error("High Risk")

# ------------------------------
# AGENT RESULTS
# ------------------------------
st.divider()
st.header("MAICA Agent Analysis")

# ------------------------------
# 1. REGULATION AGENT
# ------------------------------
st.subheader("📜 Regulation Agent")

for rule in report["regulation_rules"]:
    if rule["severity"] == "High":
        st.error(f"{rule['rule_id']} — {rule['description']}")
    else:
        st.warning(f"{rule['rule_id']} — {rule['description']}")

# ------------------------------
# 2. MODEL INSPECTION AGENT
# ------------------------------
st.subheader("🔍 Model Inspection Agent")

for check in report["model_inspection"]:

    if check["result"] == "Pass":
        st.success(f"{check['check']} — {check['details']}")

    elif check["result"] == "Warning":
        st.warning(f"{check['check']} — {check['details']}")

    else:
        st.error(f"{check['check']} — {check['details']}")

# ------------------------------
# 3. RUNTIME MONITORING AGENT
# ------------------------------
st.subheader("⚙ Runtime Monitoring Agent")

for alert in report["runtime_monitoring"]:
    st.warning(f"{alert['alert']} → {alert['details']}")

# ------------------------------
# 4. EXPLAINABILITY AGENT
# ------------------------------
st.subheader("🧠 Explainability Agent")

exp = report["explainability"]

st.info(
f"""
Method Used: {exp['method']}

Samples Explained: {exp['samples_explained']}

Top Influencing Features:
{", ".join(exp['top_features'][:5])}
"""
)

# ------------------------------
# FINAL SUMMARY
# ------------------------------
st.divider()
st.subheader("Final MAICA Summary")

st.write(f"Overall Compliance: **{report['summary']['overall_compliance']}**")
st.write(report["summary"]["notes"])

st.success("MAICA successfully audited the AI system.")