import random

def generate_portfolio(risk_level, amount):

    low_risk = [
        "HDFC Bank", "ITC", "Infosys", "Tata Steel",
        "Nestle India", "Power Grid", "Asian Paints"
    ]

    medium_risk = [
        "Reliance Industries", "TCS", "ICICI Bank", "HUL",
        "Larsen & Toubro", "Bharti Airtel", "Maruti Suzuki"
    ]

    high_risk = [
        "Tesla", "Nvidia", "Amazon", "Adani Enterprises",
        "Zomato", "Paytm", "BYD"
    ]

    if risk_level == "Low":
        stocks = random.sample(low_risk, 3)
    elif risk_level == "High":
        stocks = random.sample(high_risk, 3)
    else:
        stocks = random.sample(medium_risk, 3)

    weights = [random.uniform(0.2, 0.5) for _ in range(3)]
    total = sum(weights)
    weights = [w / total for w in weights]

    portfolio = {}

    for i, stock in enumerate(stocks):
        portfolio[stock] = int(amount * weights[i])

    strategy = f"{risk_level} risk strategy dynamically generated with diversified allocation."

    return portfolio, strategy