from pydantic import BaseModel
from typing import List

class StockInsightRequest(BaseModel):
    stock_symbol: str  # e.g., "AAPL" (case-insensitive)
    days: int          # Number of days for predictions (e.g., 5)

class StockPrediction(BaseModel):
    date: str          # Date of the prediction
    predicted_price: float  # Predicted stock price

class StockInsightResponse(BaseModel):
    stock_symbol: str
    current_price: float
    predictions: List[StockPrediction]
    data_source: str  # API provider used for fetching stock data
