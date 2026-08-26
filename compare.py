import pandas as pd

from strategies.rsi_strategy import generate_signals as rsi_signals
from strategies.ema_strategy import generate_signals as ema_signals
from strategies.sma_strategy import generate_signals as sma_signals
from strategies.macd_strategy import generate_signals as macd_signals
from strategies.stochastic_strategy import generate_signals as stochastic_signals
from evaluation import evaluate_classification

from backtest import backtest
from metrics import evaluate_metrics

def compare_all_strategies(df):

    strategies = {
        "RSI and Volume": rsi_signals,
        "EMA Crossover": ema_signals,
        "SMA Crossover": sma_signals,
        "MACD": macd_signals,
        "Stochastic Oscillator": stochastic_signals
    }

    results = []

    for strategy_name, strategy_function in strategies.items():

        temp_df = df.copy()

        temp_df = strategy_function(temp_df)

        total_profit, trades = backtest(temp_df)

        metrics = evaluate_metrics(trades)
        classification = evaluate_classification(temp_df)

        results.append({
    "Strategy": strategy_name,
    "Accuracy (%)": round(classification["accuracy"] * 100, 2),
    "Precision": round(classification["precision"], 2),
    "Recall": round(classification["recall"], 2),
    "Sensitivity": round(classification["sensitivity"], 2),
    "F1-Score": round(classification["f1_score"], 2),
    "AUC": round(classification["auc"], 2),
    "Total Profit": round(metrics["total_profit"], 2),
    "Total Trades": metrics["total_trades"],
    "Sharpe Ratio": round(metrics["sharpe_ratio"], 2),
    "Max Drawdown": round(metrics["max_drawdown"], 2),
    "Confusion Matrix": str(classification["confusion_matrix"])
})

    return pd.DataFrame(results)