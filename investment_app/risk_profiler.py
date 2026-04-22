def determine_risk(age, income, risk_input):

    if risk_input.lower() == "high":
        return "high"

    if risk_input.lower() == "medium":
        return "medium"

    if age > 50:
        return "low"

    return "medium"