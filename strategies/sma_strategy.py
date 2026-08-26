import pandas as pd

def generate_signals(df):

    df = df.copy()

    # Calculate SMAs
    df["SMA20"] = df["close"].rolling(window=20).mean()
    df["SMA50"] = df["close"].rolling(window=50).mean()

    # Buy when SMA20 crosses above SMA50
    df["buy_signal"] = (
        (df["SMA20"] > df["SMA50"]) &
        (df["SMA20"].shift(1) <= df["SMA50"].shift(1))
    )

    # Sell when SMA20 crosses below SMA50
    df["sell_signal"] = (
        (df["SMA20"] < df["SMA50"]) &
        (df["SMA20"].shift(1) >= df["SMA50"].shift(1))
    )

    return df