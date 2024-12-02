from fastapi import APIRouter
from typing import Any
from datetime import datetime
import ccxt

from schemas.v1.crypto import TradeSignalResponse

router = APIRouter()

exchange = ccxt.binance()


def fetch_btc_usd_price() -> float:
    ticker = exchange.fetch_ticker('BTC/USDT')
    return ticker['last']


STOP_LOSS_PERCENTAGE = 2
TARGET_PRICE_PERCENTAGE = 5


def calculate_stop_loss_and_target(current_price: float) -> dict:
    stop_loss = current_price * (1 - STOP_LOSS_PERCENTAGE / 100)
    target_price = current_price * (1 + TARGET_PRICE_PERCENTAGE / 100)
    return {"stop_loss": round(stop_loss, 2), "target_price": round(target_price, 2)}


def get_trade_signal() -> dict:
    current_price = fetch_btc_usd_price()

    previous_price = current_price

    if current_price > previous_price:
        trade_signal = "buy"
    elif current_price < previous_price:
        trade_signal = "sell"
    else:
        trade_signal = "hold"

    stop_loss_and_target = calculate_stop_loss_and_target(current_price)

    return {
        "trade_signal": trade_signal,
        "current_price": current_price,
        **stop_loss_and_target
    }


@router.get("/btc-usd-signal", response_model=TradeSignalResponse, status_code=200, name="btc-usd-signal")
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
