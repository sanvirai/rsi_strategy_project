def ai_recommendation(df):

    rsi = df["RSI"].iloc[-1]

    buy = df["buy_signal"].iloc[-1]
    sell = df["sell_signal"].iloc[-1]

    if buy:
        return {
            "title": "🟢 BUY",
            "reason": (
                f"RSI = {rsi:.2f}\n\n"
                "• RSI is in the oversold region.\n"
                "• Buy signal generated.\n"
                "• Trend looks favorable."
            )
        }

    elif sell:
        return {
            "title": "🔴 SELL",
            "reason": (
                f"RSI = {rsi:.2f}\n\n"
                "• RSI is in the overbought region.\n"
                "• Sell signal generated.\n"
                "• Consider booking profits."
            )
        }

    else:
        return {
            "title": "🟡 HOLD",
            "reason": (
                f"RSI = {rsi:.2f}\n\n"
                "• No buy or sell signal.\n"
                "• Market is neutral.\n"
                "• Wait for the next opportunity."
            )
        }