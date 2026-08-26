import pandas as pd

def generate_signals(df):

    df = df.copy()

    low14 = df["low"].rolling(14).min()
    high14 = df["high"].rolling(14).max()

    df["%K"] = ((df["close"] - low14) / (high14 - low14)) * 100
    df["%D"] = df["%K"].rolling(3).mean()

    # Buy
    df["buy_signal"] = (
        (df["%K"] > df["%D"]) &
        (df["%K"].shift(1) <= df["%D"].shift(1)) &
        (df["%K"] < 20)
    )

    # Sell
    df["sell_signal"] = (
        (df["%K"] < df["%D"]) &
        (df["%K"].shift(1) >= df["%D"].shift(1)) &
        (df["%K"] > 80)
    )

    return df
