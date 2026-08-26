# RSI Strategy Project

Research and backtesting toolkit for technical-indicator trading strategies on NSE equities. It generates buy/sell signals, simulates fills with a stop-loss, reports performance metrics, and exposes an interactive Streamlit dashboard.

This repository is for **education and research**. It is not investment advice and is not a live brokerage integration.

## Features

- **RSI + volume strategy** — 9-period RSI with oversold/overbought bands, a 5% buffer, volume confirmation vs a 20-period average, and a 3-bar cooldown
- **Additional strategies** — EMA crossover (20/50), SMA crossover, MACD, and Stochastic oscillator
- **Backtester** — next-bar-open entries/exits, 2% stop-loss, SQLite trade log (`trading_data.db`)
- **Performance metrics** — total P&L, win rate, average profit, Sharpe ratio, risk/reward, max drawdown
- **Classification metrics** — accuracy, precision, recall, F1, AUC (buy signal vs next-bar up-move)
- **Dashboard** — Streamlit UI with Plotly candlesticks, RSI overlay, equity curve, alerts, and strategy comparison
- **Market data** — Yahoo Finance via `yfinance` (dashboard uses 15-minute bars; `download_data.py` pulls 1-minute samples)

## Architecture

```
                    ┌─────────────────┐
                    │  config.py      │  RSI length, bands, cooldown
                    └────────┬────────┘
                             │
  yfinance ──► live_data.py ─┴─► indicators.py ──► strategies/* ──► backtest.py
  CSV      ──► main.py                                       │
                                                             ▼
                                              metrics.py / evaluation.py
                                                             │
                    ┌──────────────┬──────────────┬──────────┴──────────┐
                    ▼              ▼              ▼                     ▼
              visualize.py   dashboard.py    database.py            alerts.py
                             (Streamlit)     (SQLite)            ai_advisor.py
```

| Path | Role |
|------|------|
| `main.py` | CLI backtest on `data/sample_data.csv` |
| `dashboard.py` | Streamlit app (primary UI) |
| `config.py` | Shared strategy parameters |
| `indicators.py` | Wilder-style RSI (EWM) |
| `strategy.py` | RSI-only signals (used by CLI) |
| `strategies/` | RSI+volume, EMA, SMA, MACD, Stochastic |
| `backtest.py` | Fill engine and persistence |
| `metrics.py` | Trade-level performance |
| `evaluation.py` | Signal classification vs next close |
| `compare.py` | Side-by-side strategy table |
| `live_data.py` | Yahoo Finance loader |
| `download_data.py` | Batch CSV download into `data/` |
| `database.py` | SQLite `trades` table |
| `visualize.py` | Matplotlib equity curve + mplfinance candles |
| `alerts.py` / `ai_advisor.py` | Latest-bar BUY / SELL / HOLD messaging |

## Requirements

- Python 3.10+ recommended
- Internet access for Yahoo Finance (dashboard and `download_data.py`)

Install:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install pandas numpy yfinance streamlit plotly matplotlib mplfinance scikit-learn
```

There is no `requirements.txt` in the repo yet; pin the above packages if you need a reproducible environment.

## Quick start

### Streamlit dashboard

```bash
streamlit run dashboard.py
```

Then:

1. Pick a ticker in the sidebar (`HDFCBANK.NS`, `RELIANCE.NS`, `INFY.NS`, `TCS.NS`, `ITC.NS`, `KOTAKBANK.NS`).
2. Choose a strategy, or **Compare All Strategies**.
3. Review alerts, AI-style commentary, P&L metrics, candlesticks, RSI, equity curve, and trade history.

### CLI backtest (historical CSV)

Place OHLCV data at `data/sample_data.csv` with a `datetime` column (plus `open`/`high`/`low`/`close`; volume is used by the dashboard RSI+volume path). Then:

```bash
python main.py
```

Download sample NSE CSVs into `data/`:

```bash
python download_data.py
```

Smoke-test the live pipeline:

```bash
python test_dash.py
```

Inspect persisted trades:

```bash
python test_db.py
```

## Default strategy parameters

Defined in `config.py`:

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `TIMEFRAME` | `15m` | Yahoo interval for the dashboard |
| `RSI_LENGTH` | `9` | RSI lookback |
| `OVERSOLD` / `OVERBOUGHT` | `30` / `70` | RSI bands |
| `BUFFER_PERCENT` | `5` | Extra room around the bands |
| `COOLDOWN_BARS` | `3` | Minimum bars between like signals |
| `TARGET1` / `TARGET2` | `0.5` / `1.0` | Percent targets (config only; backtester currently uses a 2% stop) |

**RSI + volume (dashboard):** buy when RSI is oversold, turning up, and volume is above its 20-period mean; sell when RSI is overbought, turning down, and volume is elevated.

**CLI `strategy.py`:** same RSI logic **without** the volume filter.

**Backtest fills:** signal on bar `i` executes at bar `i+1` open; long-only; 2% stop vs entry; remaining position marked at the last close.

## Data

- Dashboard: ~1 month of 15-minute bars from Yahoo Finance.
- `download_data.py`: 5 days of 1-minute bars for the same NSE names, written as `data/*.csv`.
- `.gitignore` excludes `.env`, `*.db`, and `__pycache__/`. Do not commit `trading_data.db`.

## Limitations

- No slippage, commissions, or position sizing beyond quantity `1`.
- Classification metrics treat every non-buy bar as a negative; they are not a full trade-outcome model.
- `ai_advisor.py` is rule-based (RSI + last signal), not an LLM.
- Yahoo intervals and NSE symbols can fail outside market hours or if the API rate-limits.

## License

No license file is included. All rights remain with the repository owner unless a license is added.

## Disclaimer

Past backtest results do not predict future returns. Markets involve risk of loss. Use this code only for learning, research, and paper evaluation.
