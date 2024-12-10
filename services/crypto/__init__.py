
STOP_LOSS_PERCENTAGE = 2
TARGET_PRICE_PERCENTAGE = 5


def calculate_stop_loss_and_target(current_price: float) -> dict:
    stop_loss = current_price * (1 - STOP_LOSS_PERCENTAGE / 100)
    target_price = current_price * (1 + TARGET_PRICE_PERCENTAGE / 100)
    return {"stop_loss": round(stop_loss, 2), "target_price": round(target_price, 2)}

