from fastapi import APIRouter, HTTPException

from schemas.v1.stock import StockInsightRequest, StockInsightResponse
from services.stock import fetch_real_time_stock_data, generate_stock_predictions

router = APIRouter()


@router.post("/stock-insight", response_model=StockInsightResponse)
async def get_stock_insight(request: StockInsightRequest):
    """
    Fetch real-time stock data and provide predictions for the specified number of days.
    """
    # Fetch real-time stock price
    try:
        current_price = fetch_real_time_stock_data(request.stock_symbol.upper())
    except HTTPException as e:
        raise e

    # Generate predictions
    predictions = generate_stock_predictions(current_price, request.days)

    # Prepare response
    response = StockInsightResponse(
        stock_symbol=request.stock_symbol.upper(),
        current_price=current_price,
        predictions=predictions,
        data_source="Alpha Vantage"
    )
    return response
