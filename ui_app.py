import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MAICA Dashboard", layout="wide")

st.title("MAICA - AI Compliance Auditing System")
st.markdown("### Multi-Domain Compliance Dashboard")

st.divider()

# -------------------------
# SESSION STATE
# -------------------------
if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "report_type" not in st.session_state:
    st.session_state.report_type = None


# -------------------------
# DOMAIN SELECTION
# -------------------------
domain = st.selectbox(
    "Select Dataset Domain",
    ["Healthcare", "Finance"]
)

report_type = st.selectbox(
    "Select Report Type",
    ["Security Report", "Compliance Report"]
)

st.divider()

# -------------------------
# FILE PATH
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_map = {
    "Healthcare": {
        "Security Report": os.path.join(BASE_DIR, "reports", "healthcare_security_report.json"),
        "Compliance Report": os.path.join(BASE_DIR, "reports", "healthcare_compliance_report.json")
    },
    "Finance": {
        "Security Report": os.path.join(BASE_DIR, "reports", "finance_security_report.json"),
        "Compliance Report": os.path.join(BASE_DIR, "reports", "finance_compliance_report.json")
    }
}

file_path = file_map[domain][report_type]


# -------------------------
# LOAD REPORT
# -------------------------
if st.button("Show Selected Report"):

    if os.path.exists(file_path):

        with open(file_path) as f:
            st.session_state.report_data = json.load(f)
            st.session_state.report_type = report_type

        st.success(f"{domain} - {report_type} Loaded")

    else:
        st.error("Report file not found")


# -------------------------
# DISPLAY REPORT
# -------------------------
data = st.session_state.report_data
rtype = st.session_state.report_type

if data:

    # -------------------------
    # COMPLIANCE REPORT
    # -------------------------
    if rtype == "Compliance Report":

        st.subheader("Regulation Rules")

        rules = data.get("regulation_rules", [])
        severity_list = []

        for rule in rules:

            severity = rule.get("severity", "Medium")
            severity_list.append(severity)

            if severity == "High":
                st.error(f"🔴 {rule['rule_id']} - {rule['description']}")

            elif severity == "Medium":
                st.warning(f"🟠 {rule['rule_id']} - {rule['description']}")

            else:
                st.info(f"🟢 {rule['rule_id']} - {rule['description']}")

        # -------------------------
        # COMPLIANCE SEVERITY PIE CHART
        # -------------------------
        st.subheader("Compliance Severity Distribution")

        df = pd.DataFrame({"Severity": severity_list})

        severity_counts = df["Severity"].value_counts().reset_index()
        severity_counts.columns = ["Severity", "Count"]

        fig = px.pie(
            severity_counts,
            names="Severity",
            values="Count",
            title="Regulation Rule Severity Distribution"
        )

        st.plotly_chart(fig, width="stretch")

        st.divider()

        st.subheader("Summary")

        st.metric("Overall Compliance", data["summary"]["overall_compliance"])
        st.info(data["summary"]["notes"])


    # -------------------------
    # SECURITY REPORT
    # -------------------------
    elif rtype == "Security Report":

        st.subheader("Sensitive Attributes Detected")

        sensitive = data.get("sensitive_attributes_detected", [])

        if sensitive:

            st.write(sensitive)

            st.metric("Total Sensitive Fields", data.get("count", 0))
            st.error(f"Security Status: {data.get('security_status')}")

            # -------------------------
            # SENSITIVE ATTRIBUTE CHART
            # -------------------------
            df_sensitive = pd.DataFrame({
                "Attribute": sensitive,
                "Risk": [1] * len(sensitive)
            })

            fig = px.bar(
                df_sensitive,
                y="Attribute",
                x="Risk",
                orientation="h",
                color="Attribute",
                title="Sensitive Attribute Risk Indicators"
            )

            st.plotly_chart(fig, width="stretch")

        else:
            st.success("No Sensitive Attributes Detected")

        st.divider()

        st.write("Recommendation")
        st.info(data.get("recommendation", "No recommendation available"))


# -------------------------
# MODEL PERFORMANCE
# -------------------------
st.divider()

st.subheader("📊 Model Performance")

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        names=["Correct Predictions", "Errors"],
        values=[91.6, 8.4],
        title="Healthcare Model Accuracy"
    )

    st.plotly_chart(fig, width="stretch")

with col2:

    fig = px.pie(
        names=["Correct Predictions", "Errors"],
        values=[87, 13],
        title="Finance Model Accuracy"
    )

    st.plotly_chart(fig, width="stretch")

st.success("System Ready for Audit Review")