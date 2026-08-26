from config import (
    OVERSOLD,
    OVERBOUGHT,
    BUFFER_PERCENT,
    COOLDOWN_BARS
)

def generate_signals(df):

    df["volume_ma"] = df["volume"].rolling(window=20).mean()
    df["high_volume"] = df["volume"] > df["volume_ma"]

    df['rsi_up'] = df['RSI'] > df['RSI'].shift(1)

    df['rsi_up'] = df['RSI'] > df['RSI'].shift(1)
    df['rsi_down'] = df['RSI'] < df['RSI'].shift(1)

    df['buy_raw'] = (
    (df['RSI'] < OVERSOLD) &
    df['rsi_up'] &
    df['high_volume'] &
    (df['RSI'] <= OVERSOLD + (OVERSOLD * BUFFER_PERCENT / 100))
    )
    
    df['sell_raw'] = (
    (df['RSI'] > OVERBOUGHT) &
    df['rsi_down'] &
    df['high_volume'] &
    (df['RSI'] >= OVERBOUGHT - (OVERBOUGHT * BUFFER_PERCENT / 100))
    )

    
    last_buy = -100
    last_sell = -100
    buy_signals = []
    sell_signals = []

    for i in range(len(df)):
        buy = False
        sell = False

        if df['buy_raw'].iloc[i] and (i - last_buy >= COOLDOWN_BARS):
            buy = True
            last_buy = i

        if df['sell_raw'].iloc[i] and (i - last_sell >= COOLDOWN_BARS):
            sell = True
            last_sell = i

        buy_signals.append(buy)
        sell_signals.append(sell)

    df['buy_signal'] = buy_signals
    df['sell_signal'] = sell_signals

    return df