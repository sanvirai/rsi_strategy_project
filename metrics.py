import numpy as np


def evaluate_metrics(trades):

    if len(trades) == 0:
        return {
            "total_profit": 0,
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "average_profit": 0,
            "risk_reward": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0
        }

    profits = [t["profit"] for t in trades]

    total_profit = sum(profits)
    total_trades = len(profits)

    winning_trades = len([p for p in profits if p > 0])
    losing_trades = len([p for p in profits if p < 0])

    win_rate = (winning_trades / total_trades) * 100

    average_profit = np.mean(profits)

    avg_win = (
        np.mean([p for p in profits if p > 0])
        if winning_trades else 0
    )

    avg_loss = (
        abs(np.mean([p for p in profits if p < 0]))
        if losing_trades else 0
    )

    risk_reward = (
        avg_win / avg_loss
        if avg_loss != 0 else 0
    )

    # Annualized Sharpe Ratio
    std_profit = np.std(profits)

    sharpe_ratio = (
        (np.mean(profits) / std_profit) * np.sqrt(252)
        if std_profit != 0 else 0
    )

    # Drawdown calculation
    initial_capital = 100000

    equity = initial_capital + np.cumsum(profits)

    peak = np.maximum.accumulate(equity)

    drawdown = ((equity - peak) / peak) * 100

    max_drawdown = abs(min(drawdown)) if len(drawdown) else 0


    return {
        "total_profit": total_profit,
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "average_profit": average_profit,
        "risk_reward": risk_reward,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown
    }