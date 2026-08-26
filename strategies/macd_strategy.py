import pandas as pd

def generate_signals(df):

    df = df.copy()

    # MACD
    df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Buy
    df["buy_signal"] = (
        (df["MACD"] > df["Signal"]) &
        (df["MACD"].shift(1) <= df["Signal"].shift(1))
    )

    # Sell
    df["sell_signal"] = (
        (df["MACD"] < df["Signal"]) &
        (df["MACD"].shift(1) >= df["Signal"].shift(1))
    )

    return df