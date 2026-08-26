def generate_alert(df):
    """
    Returns the latest trading alert.
    """

    latest = df.iloc[-1]

    if latest["buy_signal"]:
        return "🟢 BUY SIGNAL"

    elif latest["sell_signal"]:
        return "🔴 SELL SIGNAL"

    else:
        return "🟡 HOLD"