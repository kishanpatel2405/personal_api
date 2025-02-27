from fastapi import APIRouter, HTTPException, Query

from schemas.v1.stock import (
    RealTimeStockDataResponse,
    StockInsightRequest,
    StockInsightResponse,
    StockPredictionResponse,
    StockSymbol,
)
from services.stock import fetch_real_time_stock_data, generate_stock_predictions

router = APIRouter()


@router.get(
    "/real-time-data", response_model=RealTimeStockDataResponse, status_code=200
)
async def get_real_time_stock_data(stock_symbol: StockSymbol):
    try:
        current_price = fetch_real_time_stock_data(stock_symbol)
    except HTTPException as e:
        raise e

    return RealTimeStockDataResponse(
        stock_symbol=stock_symbol,
        current_price=current_price,
        data_source="Alpha Vantage",
    )


@router.get(
    "/stock-predictions", response_model=StockPredictionResponse, status_code=200
)
async def get_stock_predictions(
    stock_symbol: StockSymbol,
    current_price: float = Query(
        ..., description="The current price of the stock", example=150.0
    ),
    days: int = Query(
        ..., ge=1, le=30, description="Number of days to predict", example=5
    ),
):
    predictions = generate_stock_predictions(stock_symbol, current_price, days)

    return StockPredictionResponse(stock_symbol=stock_symbol, predictions=predictions)


@router.post("/stock-insight", response_model=StockInsightResponse, status_code=200)
async def get_stock_insight(request: StockInsightRequest):
    try:
        current_price = fetch_real_time_stock_data(request.stock_symbol)
    except HTTPException as e:
        raise e

    predictions = generate_stock_predictions(
        request.stock_symbol, current_price, request.days
    )

    return StockInsightResponse(
        stock_symbol=request.stock_symbol,
        current_price=current_price,
        predictions=predictions,
        data_source="Alpha Vantage",
    )
