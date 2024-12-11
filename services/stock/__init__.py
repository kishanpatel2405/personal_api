from datetime import datetime, timedelta
from random import random

import requests
from fastapi import HTTPException

ALPHA_VANTAGE_API_KEY = "RROYVFSHLQKFO5RV"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"


def fetch_real_time_stock_data(stock_symbol: str) -> float:
    """
    Fetch the real-time price for a stock, cryptocurrency, or forex symbol.
    """
    # Determine the appropriate Alpha Vantage function based on symbol type
    if "/" in stock_symbol:  # Forex or Crypto (e.g., BTC/USD, EUR/USD)
        if "BTC" in stock_symbol or "ETH" in stock_symbol:  # Crypto
            function = "CURRENCY_EXCHANGE_RATE"
            from_currency, to_currency = stock_symbol.split("/")
        else:  # Forex
            function = "CURRENCY_EXCHANGE_RATE"
            from_currency, to_currency = stock_symbol.split("/")

        response = requests.get(
            ALPHA_VANTAGE_BASE_URL,
            params={
                "function": function,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "apikey": ALPHA_VANTAGE_API_KEY
            }
        )
        key = "Realtime Currency Exchange Rate"
        price_key = "5. Exchange Rate"
    else:  # Stock (e.g., AAPL)
        function = "GLOBAL_QUOTE"
        response = requests.get(
            ALPHA_VANTAGE_BASE_URL,
            params={
                "function": function,
                "symbol": stock_symbol,
                "apikey": ALPHA_VANTAGE_API_KEY
            }
        )
        key = "Global Quote"
        price_key = "05. price"

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage.")

    data = response.json()
    if key not in data or price_key not in data[key]:
        raise HTTPException(status_code=404, detail=f"Symbol '{stock_symbol}' not found or invalid.")

    return float(data[key][price_key])


def fetch_historical_stock_data(stock_symbol: str, days: int):
    """
    Fetch historical stock data for a given stock symbol and number of days.
    """
    response = requests.get(
        ALPHA_VANTAGE_BASE_URL,
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_symbol,
            "apikey": ALPHA_VANTAGE_API_KEY,
            "outputsize": "compact"  # Fetch last 100 data points
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch stock data.")

    data = response.json()
    if "Time Series (Daily)" not in data:
        raise HTTPException(status_code=404, detail=f"Stock symbol '{stock_symbol}' not found.")

    time_series = data["Time Series (Daily)"]
    historical_prices = []

    for date, stats in list(time_series.items())[:days]:  # Fetch last `days` data points
        historical_prices.append(float(stats["4. close"]))

    return historical_prices


def generate_stock_predictions(stock_symbol: str, current_price: float, days: int) -> list:
    """
    Generate stock predictions based on historical data and trend analysis.
    """
    # Fetch historical data
    historical_prices = fetch_historical_stock_data(stock_symbol, days)

    # Simple prediction model: calculate the average change over the last N days
    price_changes = [historical_prices[i] - historical_prices[i - 1] for i in range(1, len(historical_prices))]
    avg_change = sum(price_changes) / len(price_changes) if price_changes else 0

    predictions = []
    for i in range(1, days + 1):
        predicted_price = current_price + (avg_change * i)  # Use the average change to project price

        # Determine trading signal (Buy/Sell/Hold based on predicted price)
        signal = "Hold"
        if predicted_price > current_price * 1.02:  # Price > 2% increase
            signal = "Buy"
        elif predicted_price < current_price * 0.98:  # Price > 2% decrease
            signal = "Sell"

        predicted_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        predictions.append({
            "date": predicted_date,
            "predicted_price": round(predicted_price, 2),
            "signal": signal
        })

    return predictions
