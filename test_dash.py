#!/usr/bin/env python
import sys
import traceback

try:
    from live_data import get_live_data
    from indicators import calculate_rsi
    from config import RSI_LENGTH
    from strategies.rsi_strategy import generate_signals as rsi_signals
    from backtest import backtest
    from metrics import evaluate_metrics
    
    print("Loading data...")
    df = get_live_data()
    print(f"✓ Data loaded: {df.shape}")
    print(f"✓ Columns: {df.columns.tolist()}")
    
    print("\nProcessing datetime...")
    import pandas as pd
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.set_index("datetime", inplace=True)
        print("✓ Datetime processed and set as index")
    else:
        print(f"✗ ERROR: datetime column not found. Available: {df.columns.tolist()}")
        sys.exit(1)
    
    print("\nCalculating RSI...")
    df["RSI"] = calculate_rsi(df, RSI_LENGTH)
    print("✓ RSI calculated")
    
    print("\nGenerating signals...")
    df = rsi_signals(df)
    print("✓ Signals generated")
    
    print("\nBacktesting...")
    total_profit, trades = backtest(df)
    print(f"✓ Backtest complete: {len(trades)} trades, ₹{total_profit:.2f} profit")
    
    print("\nAll checks passed! ✓✓✓")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
