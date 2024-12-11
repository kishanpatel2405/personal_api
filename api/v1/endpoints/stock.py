from fastapi import APIRouter, HTTPException
from schemas.v1.stock import (
    StockInsightRequest,
    StockInsightResponse,
    RealTimeStockDataRequest,
    RealTimeStockDataResponse,
    StockPredictionRequest,
    StockPredictionResponse,
)
from services.stock import fetch_real_time_stock_data, generate_stock_predictions

router = APIRouter()


@router.post("/stock-insight", response_model=StockInsightResponse, status_code=200, name="stock_insight")
async def get_stock_insight(request: StockInsightRequest):

    try:
        current_price = fetch_real_time_stock_data(request.stock_symbol.upper())
    except HTTPException as e:
        raise e

    predictions = generate_stock_predictions(current_price, request.days)

    response = StockInsightResponse(
        stock_symbol=request.stock_symbol.upper(),
        current_price=current_price,
        predictions=predictions,
        data_source="Alpha Vantage"
    )
    return response


@router.post("/real-time-data", response_model=RealTimeStockDataResponse, status_code=200, name="real_time_data")
async def get_real_time_stock_data(request: RealTimeStockDataRequest):
    try:
        current_price = fetch_real_time_stock_data(request.stock_symbol.upper())
    except HTTPException as e:
        raise e

    return RealTimeStockDataResponse(
        stock_symbol=request.stock_symbol.upper(),
        current_price=current_price,
        data_source="Alpha Vantage"
    )


@router.post("/stock-predictions", response_model=StockPredictionResponse, status_code=200, name="stock_predictions")
async def get_stock_predictions(request: StockPredictionRequest):
    """
    Generate stock predictions based on current price.
    """
    predictions = generate_stock_predictions(request.current_price, request.days)

    return StockPredictionResponse(
        stock_symbol=request.stock_symbol.upper(),
        predictions=predictions
    )
