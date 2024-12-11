from pydantic import BaseModel, Field
from typing import List


class StockInsightRequest(BaseModel):
    stock_symbol: str = Field(..., description="Stock symbol, e.g., AAPL")
    days: int = Field(..., description="Number of days to predict")


class StockInsightResponse(BaseModel):
    stock_symbol: str
    current_price: float
    predictions: List[float]
    data_source: str


class RealTimeStockDataRequest(BaseModel):
    stock_symbol: str = Field(..., description="Stock symbol, e.g., AAPL")


class RealTimeStockDataResponse(BaseModel):
    stock_symbol: str
    current_price: float
    data_source: str


class StockPredictionRequest(BaseModel):
    stock_symbol: str = Field(..., description="Stock symbol, e.g., AAPL")
    current_price: float = Field(..., description="Current stock price")
    days: int = Field(..., description="Number of days to predict")


class StockPredictionResponse(BaseModel):
    stock_symbol: str
    predictions: List[float]
