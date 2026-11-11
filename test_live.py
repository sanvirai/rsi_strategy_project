from live_data import get_live_data
from indicators import calculate_rsi
from strategies.rsi_strategy import generate_signals
from backtest import backtest
from metrics import evaluate_metrics
from config import RSI_LENGTH
import pandas as pd

print("=" * 60)
print("   LIVE MARKET DATA TEST (Yahoo Finance - RELIANCE.NS)")
print("=" * 60)

df = get_live_data("RELIANCE.NS", interval="15m", period="1mo")

if df is None or df.empty:
    print("ERROR: No live data returned!")
else:
    print(f"Live candles fetched : {len(df)}")
    print(f"Columns              : {list(df.columns)}")

    # Set index if needed
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime")

    print(f"Date range           : {df.index[0]}  -->  {df.index[-1]}")
    print(f"Latest Close         : ₹{df['close'].iloc[-1]:.2f}")
    print(f"Latest Volume        : {int(df['volume'].iloc[-1]):,}")

    # Run strategy on live data
    df["RSI"] = calculate_rsi(df, RSI_LENGTH)
    df = generate_signals(df)
    total_pnl, trades = backtest(df)
    metrics = evaluate_metrics(trades)

    print("\n" + "=" * 60)
    print("LIVE BACKTEST PERFORMANCE (last 1 month of 15m data)")
    print("=" * 60)
    print(f"Total Profit      : Rs {metrics['total_profit']:.2f}")
    print(f"Total Trades      : {metrics['total_trades']}")
    print(f"Winning Trades    : {metrics['winning_trades']}")
    print(f"Losing Trades     : {metrics['losing_trades']}")
    print(f"Win Rate          : {metrics['win_rate']:.2f}%")
    print(f"Average Profit    : Rs {metrics['average_profit']:.2f}")
    print(f"Sharpe Ratio      : {metrics['sharpe_ratio']:.2f}")
    print(f"Risk Reward Ratio : {metrics['risk_reward']:.2f}")
    print(f"Maximum Drawdown  : Rs {metrics['max_drawdown']:.2f}")
    print("=" * 60)

    # Compare sample vs live
    sample = pd.read_csv("data/sample_data.csv")
    sample.columns = sample.columns.str.strip().str.lower()
    sample["datetime"] = pd.to_datetime(sample["datetime"])
    sample = sample.set_index("datetime")
    sample["RSI"] = calculate_rsi(sample, RSI_LENGTH)
    from strategies.rsi_strategy import generate_signals as rsi_gen
    sample = rsi_gen(sample)
    _, sample_trades = backtest(sample)
    sample_metrics = evaluate_metrics(sample_trades)

    print("\n" + "=" * 60)
    print("COMPARISON: SAMPLE DATA  vs  LIVE RELIANCE.NS DATA")
    print("=" * 60)
    print(f"{'Metric':<22} {'Sample Data':>14} {'Live Data':>14}")
    print("-" * 52)
    print(f"{'Total Profit (Rs)':<22} {sample_metrics['total_profit']:>14.2f} {metrics['total_profit']:>14.2f}")
    print(f"{'Total Trades':<22} {sample_metrics['total_trades']:>14} {metrics['total_trades']:>14}")
    print(f"{'Win Rate (%)':<22} {sample_metrics['win_rate']:>14.2f} {metrics['win_rate']:>14.2f}")
    print(f"{'Sharpe Ratio':<22} {sample_metrics['sharpe_ratio']:>14.2f} {metrics['sharpe_ratio']:>14.2f}")
    print(f"{'Max Drawdown (Rs)':<22} {sample_metrics['max_drawdown']:>14.2f} {metrics['max_drawdown']:>14.2f}")
    print(f"{'Risk Reward Ratio':<22} {sample_metrics['risk_reward']:>14.2f} {metrics['risk_reward']:>14.2f}")
    print("=" * 60)
