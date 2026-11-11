from database import create_database, save_trade, clear_trades


def backtest(df):

    create_database()
    clear_trades()

    position = 0
    entry_price = 0
    entry_index = None
    stop_loss = 0

    quantity = 1

    total_profit = 0
    trades = []

    for i in range(len(df) - 1):

        next_open = df["open"].iloc[i + 1]

        # BUY at next candle open
        if df["buy_signal"].iloc[i] and position == 0:

            position = 1
            entry_price = next_open
            entry_index = i + 1

            # 2% stop loss
            stop_loss = entry_price * 0.98


        # STOP LOSS CHECK
        elif position == 1 and df["low"].iloc[i] <= stop_loss:

            exit_price = next_open

            profit = (exit_price - entry_price) * quantity
            total_profit += profit

            trades.append({
                "entry_time": df.index[entry_index],
                "exit_time": df.index[i + 1],
                "entry": entry_price,
                "exit": exit_price,
                "profit": profit
            })

            save_trade(
                buy_price=float(entry_price),
                sell_price=float(exit_price),
                profit=float(profit),
                trade_time=str(df.index[i + 1])
            )

            position = 0
            entry_price = 0
            entry_index = None
            stop_loss = 0


        # NORMAL SELL SIGNAL
        elif df["sell_signal"].iloc[i] and position == 1:

            exit_price = next_open

            profit = (exit_price - entry_price) * quantity
            total_profit += profit

            trades.append({
                "entry_time": df.index[entry_index],
                "exit_time": df.index[i + 1],
                "entry": entry_price,
                "exit": exit_price,
                "profit": profit
            })

            save_trade(
                buy_price=float(entry_price),
                sell_price=float(exit_price),
                profit=float(profit),
                trade_time=str(df.index[i + 1])
            )

            position = 0
            entry_price = 0
            entry_index = None
            stop_loss = 0


    # Close remaining open trade
    if position == 1:

        exit_price = df["close"].iloc[-1]

        profit = (exit_price - entry_price) * quantity
        total_profit += profit

        trades.append({
            "entry_time": df.index[entry_index],
            "exit_time": df.index[-1],
            "entry": entry_price,
            "exit": exit_price,
            "profit": profit
        })

        save_trade(
            buy_price=float(entry_price),
            sell_price=float(exit_price),
            profit=float(profit),
            trade_time=str(df.index[-1])
        )


    return total_profit, trades