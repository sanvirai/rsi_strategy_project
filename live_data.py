import yfinance as yf
import pandas as pd
from config import TIMEFRAME

def get_live_data(symbol="RELIANCE.NS", interval=TIMEFRAME, period="1mo"):

    df = yf.download(
        tickers=symbol,
        interval=interval,
        period=period,
        auto_adjust=False,
        progress=False
    )

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reset index so Datetime becomes a column
    df.reset_index(inplace=True)
    
    # Convert column names to lowercase
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # Ensure datetime column exists
    if "date" in df.columns:
        df.rename(columns={"date": "datetime"}, inplace=True)

    return df