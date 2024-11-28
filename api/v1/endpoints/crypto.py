from fastapi import APIRouter
from typing import Any
from datetime import datetime
import ccxt

from schemas.v1.crypto import TradeSignalResponse

# Initialize the API Router
router = APIRouter()

# Initialize the exchange (use Binance for BTC/USDT pair)
exchange = ccxt.binance()


# Define a function to fetch BTC/USD price
def fetch_btc_usd_price() -> float:
    ticker = exchange.fetch_ticker('BTC/USDT')  # Using USDT as it's commonly used for USD pair
    return ticker['last']


# Define the stop loss and target price percentages
STOP_LOSS_PERCENTAGE = 2  # 2% below the current price
TARGET_PRICE_PERCENTAGE = 5  # 5% above the current price


# Define a function to calculate stop loss and target price
def calculate_stop_loss_and_target(current_price: float) -> dict:
    stop_loss = current_price * (1 - STOP_LOSS_PERCENTAGE / 100)
    target_price = current_price * (1 + TARGET_PRICE_PERCENTAGE / 100)
    return {"stop_loss": round(stop_loss, 2), "target_price": round(target_price, 2)}


# Define a function to determine the trade signal
def get_trade_signal() -> dict:
    current_price = fetch_btc_usd_price()

    # Fetch previous price (this could be from a database or from past API calls)
    previous_price = current_price  # In real case, store and fetch previous values

    # Example condition for trading signal: simple price comparison
    if current_price > previous_price:
        trade_signal = "buy"
    elif current_price < previous_price:
        trade_signal = "sell"
    else:
        trade_signal = "hold"

    # Calculate stop loss and target price
    stop_loss_and_target = calculate_stop_loss_and_target(current_price)

    return {
        "trade_signal": trade_signal,
        "current_price": current_price,
        **stop_loss_and_target
    }


# Endpoint to return the BTC/USD trade signal with stop loss and target price
@router.get("/btc-usd-signal", response_model=TradeSignalResponse)
async def get_btc_usd_signal() -> Any:
    signal_data = get_trade_signal()
    return TradeSignalResponse(
        timestamp=datetime.utcnow().isoformat(),
        symbol="BTC/USD",
        trade_signal=signal_data["trade_signal"],
        current_price=signal_data["current_price"],
        stop_loss=signal_data["stop_loss"],
        target_price=signal_data["target_price"]
    )
