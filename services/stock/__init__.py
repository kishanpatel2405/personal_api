import StockPrediction
import requests
from fastapi import HTTPException
from datetime import datetime, timedelta
import random

ALPHA_VANTAGE_API_KEY = "RROYVFSHLQKFO5RV"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"


def fetch_real_time_stock_data(stock_symbol: str) -> float:
    response = requests.get(
        ALPHA_VANTAGE_BASE_URL,
        params={
            "function": "GLOBAL_QUOTE",
            "symbol": stock_symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch stock data.")

    data = response.json()
    if "Global Quote" not in data or "05. price" not in data["Global Quote"]:
        raise HTTPException(status_code=404, detail=f"Stock symbol '{stock_symbol}' not found.")

    return float(data["Global Quote"]["05. price"])


def generate_stock_predictions(current_price: float, days: int) -> list:
    predictions = []
    for i in range(1, days + 1):
        change = random.uniform(-5, 5)
        predicted_price = round(current_price + change, 2)
        predicted_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        predictions.append(StockPrediction(date=predicted_date, predicted_price=predicted_price))
    return predictions
