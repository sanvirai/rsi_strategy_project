import pandas as pd

def generate_signals(df):

    df = df.copy()

    # Calculate EMAs
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    # Buy when EMA20 crosses above EMA50
    df["buy_signal"] = (
        (df["EMA20"] > df["EMA50"]) &
        (df["EMA20"].shift(1) <= df["EMA50"].shift(1))
    )

    # Sell when EMA20 crosses below EMA50
    df["sell_signal"] = (
        (df["EMA20"] < df["EMA50"]) &
        (df["EMA20"].shift(1) >= df["EMA50"].shift(1))
    )

    return df