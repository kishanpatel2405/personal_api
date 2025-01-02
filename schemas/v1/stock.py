from typing import List

from pydantic import BaseModel, Field

from utils.enums import StockSymbol


class StockInsightRequest(BaseModel):
    stock_symbol: StockSymbol = Field(..., description="Stock symbol", example="AAPL")
    days: int = Field(..., ge=1, le=30, description="Number of days for prediction", example=5)


class StockInsightResponse(BaseModel):
    stock_symbol: StockSymbol
    current_price: float
    predictions: List[dict]  # Example: {"date": "2023-12-01", "predicted_price": 150.0}
    data_source: str


class RealTimeStockDataResponse(BaseModel):
    stock_symbol: StockSymbol
    current_price: float
    data_source: str


class StockPredictionResponse(BaseModel):
    stock_symbol: StockSymbol
    predictions: List[dict]  # Example: {"date": "2023-12-01", "predicted_price": 150.0}
