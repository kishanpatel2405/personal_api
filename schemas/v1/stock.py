from pydantic import BaseModel
from typing import List


class StockInsightRequest(BaseModel):
    stock_symbol: str
    days: int


class StockPrediction(BaseModel):
    date: str
    predicted_price: float


class StockInsightResponse(BaseModel):
    stock_symbol: str
    current_price: float
    predictions: List[StockPrediction]
    data_source: str
