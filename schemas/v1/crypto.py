from pydantic import BaseModel


class TradeSignalResponse(BaseModel):
    timestamp: str
    symbol: str
    trade_signal: str
    current_price: float
    stop_loss: float
    target_price: float

    class Config:
        orm_mode = True
