import pandas as pd

from config import RSI_LENGTH
from indicators import calculate_rsi
from strategies.rsi_strategy import generate_signals
from backtest import backtest
from metrics import evaluate_metrics
from visualize import visualize_trades

print("=" * 60)
print("      RSI & VOLUME BASED TRADING SYSTEM")
print("=" * 60)

# Load Historical Data
df = pd.read_csv("data/sample_data.csv")
df.columns = df.columns.str.strip().str.lower()

df["datetime"] = pd.to_datetime(df["datetime"])
df.set_index("datetime", inplace=True)

print("Market data loaded successfully.")

# Calculate RSI
df["RSI"] = calculate_rsi(df, RSI_LENGTH)
print("RSI calculated successfully.")

# Generate Signals
df = generate_signals(df)
print("Trading signals generated.")

# Backtesting
total_pnl, trades = backtest(df)

# Performance Metrics
metrics = evaluate_metrics(trades)

print("\n" + "=" * 60)
print("PERFORMANCE SUMMARY")
print("=" * 60)
print(f"Total Profit      : ₹{metrics['total_profit']:.2f}")
print(f"Total Trades      : {metrics['total_trades']}")
print(f"Winning Trades    : {metrics['winning_trades']}")
print(f"Losing Trades     : {metrics['losing_trades']}")
print(f"Win Rate          : {metrics['win_rate']:.2f}%")
print(f"Average Profit    : ₹{metrics['average_profit']:.2f}")
print(f"Sharpe Ratio      : {metrics['sharpe_ratio']:.2f}")
print(f"Risk Reward Ratio : {metrics['risk_reward']:.2f}")
print(f"Maximum Drawdown  : ₹{metrics['max_drawdown']:.2f}")
print("=" * 60)

# Visualize Results
visualize_trades(df,trades)