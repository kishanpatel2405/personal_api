from datetime import datetime
from typing import Any

import ccxt
import pandas as pd
import plotly.graph_objects as go
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from schemas.v1.crypto import TradeSignalResponse
from services.crypto import calculate_stop_loss_and_target

router = APIRouter()

exchange = ccxt.binance()


def fetch_btc_usd_price() -> float:
    ticker = exchange.fetch_ticker('BTC/USDT')
    return ticker['last']


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


def fetch_xau_usd_price() -> float:
    try:
        ticker = exchange.fetch_ticker('XAU/USDT')
        return ticker['last']
    except ccxt.BaseError as e:
        print(f"Error fetching data for XAU/USDT: {str(e)}")
        return None


def fetch_ohlc_data(symbol: str = 'XAU-USDT', timeframe: str = '1h') -> pd.DataFrame:
    ohlc_data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    df = pd.DataFrame(ohlc_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def generate_candlestick_chart(df: pd.DataFrame) -> str:
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlestick',
    )])

    fig.update_layout(
        title='XAU/USD Candlestick Chart',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    return fig.to_html(full_html=False)


@router.get("/xau-usd-chart", response_class=HTMLResponse, status_code=200, name="xau-usd-chart")
async def get_xau_usd_chart():
    ohlc_data = fetch_ohlc_data()

    chart_html = generate_candlestick_chart(ohlc_data)

    return HTMLResponse(content=chart_html)





