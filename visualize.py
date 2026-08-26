import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def visualize_trades(df, trades):

    # -------- Equity Curve --------
    trade_df = pd.DataFrame(trades)

    if not trade_df.empty:
        trade_df["cumulative_pnl"] = trade_df["profit"].cumsum()

        plt.figure(figsize=(10,5))
        plt.plot(
            trade_df.index,
            trade_df["cumulative_pnl"],
            marker="o",
            linewidth=2
        )

        plt.title("Equity Curve")
        plt.xlabel("Trade Number")
        plt.ylabel("Cumulative Profit")
        plt.grid(True)
        plt.show()

    # -------- Candlestick Chart --------
    mpf.plot(
    df.tail(200),
    type="candle",
    style="yahoo",
    volume=True,
    title="RSI Trading Strategy",
    figsize=(12,8)
)