import yfinance as yf

# -------------------------
# STOCK SYMBOL MAP
# -------------------------
STOCK_SYMBOLS = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Tata Consultancy Services": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ITC": "ITC.NS",
    "HUL": "HINDUNILVR.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Larsen & Toubro": "LT.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Nestle India": "NESTLEIND.NS",
    "Power Grid": "POWERGRID.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Tata Steel": "TATASTEEL.NS",

    # US Stocks
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Adani Enterprises": "ADANIENT.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm": "PAYTM.NS",
    "BYD": "BYDDF"
}


# -------------------------
# FETCH STOCK
# -------------------------
def get_stock_info(symbol):

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return 0, "-", 0

        price = round(data["Close"].iloc[-1], 2)
        open_price = round(data["Open"].iloc[-1], 2)

        change = price - open_price
        percent = round((change / open_price) * 100, 2)

        trend = "↑" if change > 0 else "↓"

        return price, trend, percent

    except:
        return 0, "-", 0


# -------------------------
# MAIN FUNCTION
# -------------------------
def get_market_snapshot(portfolio):

    result = []

    for stock_name in portfolio.keys():

        symbol = STOCK_SYMBOLS.get(stock_name)

        if not symbol:
            continue

        price, trend, percent = get_stock_info(symbol)

        result.append({
            "name": stock_name,
            "price": price,
            "trend": trend,
            "percent": percent
        })

    return result