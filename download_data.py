import yfinance as yf
import os

stocks = {
    "HDFCBANK": "HDFCBANK.NS",
    "RELIANCE": "RELIANCE.NS",
    "INFY": "INFY.NS",
    "TCS": "TCS.NS",
    "ITC": "ITC.NS",
    "KOTAKBANK": "KOTAKBANK.NS"
}

if not os.path.exists("data"):
    os.makedirs("data")

for name, ticker in stocks.items():

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        interval="1m",
        period="5d",
        group_by="column"
    )

    if isinstance(df.columns, type(yf.download("RELIANCE.NS", period="1d").columns)):
        try:
            df.columns = df.columns.get_level_values(0)
        except:
            pass

    df.reset_index(inplace=True)

    df.to_csv(f"data/{name}.csv", index=False)

print("All stock data downloaded successfully.")