import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from config import RSI_LENGTH
from indicators import calculate_rsi
from backtest import backtest
from metrics import evaluate_metrics
from alerts import generate_alert
from live_data import get_live_data
from ai_advisor import ai_recommendation
from strategies.rsi_strategy import generate_signals as rsi_signals
from strategies.ema_strategy import generate_signals as ema_signals
from strategies.sma_strategy import generate_signals as sma_signals
from strategies.macd_strategy import generate_signals as macd_signals
from strategies.stochastic_strategy import generate_signals as stochastic_signals
from compare import compare_all_strategies
from database import load_trades
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RSI Trading Dashboard",
    layout="wide"
)

st.title("📈 RSI & Volume Based Trading System")

strategy_choice = st.selectbox(
    "Select Trading Strategy",
    [
        "RSI and Volume",
        "MACD",
        "EMA Crossover",
        "SMA Crossover",
        "Stochastic Oscillator",
        "Compare All Strategies"
    ]
)
data_source = st.sidebar.radio(
    "Data Mode",
    ["Live Market (Yahoo Finance)", "Sample Data (Offline Mode)"]
)

stock = st.sidebar.selectbox(
    "Select Stock (Live Mode)",
    [
        "RELIANCE.NS",
        "HDFCBANK.NS",
        "INFY.NS",
        "TCS.NS",
        "ITC.NS",
        "KOTAKBANK.NS"
    ],
    disabled=(data_source == "Sample Data (Offline Mode)")
)

# --------------------------------------------------
# Load Data with Robust Offline Fallback
# --------------------------------------------------

def load_offline_sample():
    sample = pd.read_csv("data/sample_data.csv")
    sample.columns = sample.columns.str.strip().str.lower()
    sample["datetime"] = pd.to_datetime(sample["datetime"])
    sample = sample.set_index("datetime")
    return sample

if data_source == "Sample Data (Offline Mode)":
    df = load_offline_sample()
    st.sidebar.info("📊 Using local offline dataset (1,877 candles).")
else:
    try:
        with st.spinner(f"Fetching live data for {stock}..."):
            df = get_live_data(symbol=stock)

        if df is None or df.empty or ("datetime" not in df.columns and "date" not in df.columns):
            st.warning(f"⚠️ Live market data unavailable for {stock}. Falling back to offline sample data.")
            df = load_offline_sample()
        else:
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])
                df = df.set_index("datetime")
            elif "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")
    except Exception as e:
        st.warning(f"⚠️ Could not connect to Yahoo Finance ({e}). Running in offline sample mode.")
        df = load_offline_sample()
# --------------------------------------------------
# Run Strategy
# --------------------------------------------------

df["RSI"] = calculate_rsi(df, RSI_LENGTH)

if strategy_choice == "Compare All Strategies":
    
    comparison_df, confusion_matrices = compare_all_strategies(df)
   

    st.subheader(" Strategy Comparison")
    st.dataframe(comparison_df)

    st.subheader("Accuracy Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Accuracy (%)"]
    )

    st.subheader("Precision Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Precision"]
    )

    st.subheader(" Recall Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Recall"]
    )

    st.subheader(" Sensitivity Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Sensitivity"]
    )

    st.subheader(" F1-Score Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["F1-Score"]
    )

    st.subheader(" AUC Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["AUC"]
    )

    st.subheader(" Total Profit Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Total Profit"]
    )

    st.subheader(" Sharpe Ratio Comparison")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Sharpe Ratio"]
    )

    st.subheader(" Maximum Drawdown Comparison (₹)")
    st.bar_chart(
        comparison_df.set_index("Strategy")["Max Drawdown"]
    )
        # --------------------------------------------------
    # Separate Confusion Matrix Heatmap
    # --------------------------------------------------

    st.markdown("---")
    st.subheader("Confusion Matrix Analysis")

    selected_strategy = st.selectbox(
        "Select Strategy",
        list(confusion_matrices.keys())
    )

    cm = confusion_matrices[selected_strategy]

    if len(cm) == 2 and len(cm[0]) == 2:

        

                        
        # Row 0 (Top): Price Up -> [FN, TP]
        # Row 1 (Bottom): Price Down -> [FP, TN]
        # Col 0 (Left): Price Down | Col 1 (Right): Price Up
        matrix_data = [
            [cm[1][0], cm[1][1]],  # Top Row: FN, TP
            [cm[0][1], cm[0][0]]   # Bottom Row: FP, TN
        ]

        cell_labels = [
            [f"FN: {cm[1][0]}", f"TP: {cm[1][1]}"],
            [f"FP: {cm[0][1]}", f"TN: {cm[0][0]}"]
        ]

        fig = go.Figure(
            data=go.Heatmap(
                z=matrix_data,

                x=[
                    "Price Down",
                    "Price Up"
                ],

                y=[
                    "Price Up",
                    "Price Down"
                ],

                text=cell_labels,
                texttemplate="%{text}",
                textfont=dict(size=18),
                colorscale="Blues",
                showscale=True
            )
        )
        fig.update_layout(
            title=f"Confusion Matrix - {selected_strategy}",
            xaxis_title="Predicted Values",
            yaxis_title="Actual Values",
            height=450,
            template="plotly_white"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.write("Total observations:", sum(sum(row) for row in cm))
    else:
        st.warning("Confusion matrix must be a 2 × 2 matrix.")
    comparison_df["Score"] = (
        comparison_df["Total Profit"] * 0.5 +
        comparison_df["Sharpe Ratio"] * 0.3 -
        comparison_df["Max Drawdown"] * 0.2
    )

    best_strategy = comparison_df.sort_values(
        by="Score",
        ascending=False
    ).iloc[0]

    st.success(
        f" Best Strategy: {best_strategy['Strategy']} "
        f"(Score: {best_strategy['Score']:.2f})"
    )

    st.stop()
if strategy_choice == "RSI and Volume":
     df = rsi_signals(df)
     st.subheader("📊 Volume & Liquidity Confirmation")
     curr_vol = int(df['volume'].iloc[-1])
     avg_vol = int(df['volume_ma'].iloc[-1])
     vol_ratio = curr_vol / avg_vol if avg_vol > 0 else 1.0

     vcol1, vcol2, vcol3 = st.columns(3)
     vcol1.metric("Current 15m Volume", f"{curr_vol:,}")
     vcol2.metric("20-Period Avg Volume", f"{avg_vol:,}")
     vcol3.metric(
         "Volume Ratio (vs MA20)",
         f"{vol_ratio:.2f}x",
         delta="High Volume Confirmation" if vol_ratio > 1.0 else "Normal Volume",
         delta_color="normal" if vol_ratio > 1.0 else "off"
     )
elif strategy_choice == "EMA Crossover":
     df = ema_signals(df)

elif strategy_choice == "SMA Crossover":
    df = sma_signals(df)

elif strategy_choice == "MACD":
    df = macd_signals(df)

elif strategy_choice == "Stochastic Oscillator":
    df = stochastic_signals(df)

else:
    st.info("Invalid strategy selected.")
    st.stop()
total_profit, trades = backtest(df)

metrics = evaluate_metrics(trades)

alert = generate_alert(df)

ai_result = ai_recommendation(df)
# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------

st.success("System Loaded Successfully ✅")

st.subheader(" Trading Alert")

if "BUY" in alert:
    st.success(alert)
    

elif "SELL" in alert:
    st.error(alert)
   

else:
    st.warning(alert)

st.markdown("---")

st.subheader(" AI Trading Advisor")

st.info(ai_result["title"])

st.write(ai_result["reason"])

col1, col2, col3, col4 = st.columns(4)

col1.metric(" Total Profit", f"₹{metrics['total_profit']:.2f}")
col2.metric(" Win Rate", f"{metrics['win_rate']:.2f}%")
col3.metric(" Total Trades", str(metrics["total_trades"]))
col4.metric(" Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")

st.markdown("---")

# --------------------------------------------------
# Placeholder Charts
# --------------------------------------------------

# --------------------------------------------------
# Interactive Candlestick Chart
# --------------------------------------------------

st.subheader(" Interactive Candlestick Chart")
fig = go.Figure()

# Candlestick Price Trace
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price"
    )
)

# Overlay EMAs or SMAs if selected
if strategy_choice == "EMA Crossover" and "EMA20" in df.columns:
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA 20", line=dict(color="orange", width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], mode="lines", name="EMA 50", line=dict(color="purple", width=1.5)))

elif strategy_choice == "SMA Crossover" and "SMA20" in df.columns:
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], mode="lines", name="SMA 20", line=dict(color="#00bcd4", width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], mode="lines", name="SMA 50", line=dict(color="#e91e63", width=1.5)))

# Buy Signals
fig.add_trace(
    go.Scatter(
        x=df[df["buy_signal"]].index,
        y=df[df["buy_signal"]]["low"] * 0.998,
        mode="markers",
        marker=dict(symbol="triangle-up", size=14, color="#00e676", line=dict(width=1, color="black")),
        name="Buy Entry"
    )
)

# Sell Signals
fig.add_trace(
    go.Scatter(
        x=df[df["sell_signal"]].index,
        y=df[df["sell_signal"]]["high"] * 1.002,
        mode="markers",
        marker=dict(symbol="triangle-down", size=14, color="#ff1744", line=dict(width=1, color="black")),
        name="Sell Exit"
    )
)

fig.update_layout(
    height=550,
    xaxis_title="Timeline",
    yaxis_title="Price (₹)",
    xaxis_rangeslider_visible=False,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, width="stretch")

# --------------------------------------------------
# Interactive Volume & 20-Period MA Subplot
# --------------------------------------------------
if "volume_ma" in df.columns:
    st.subheader("📊 15m Volume & 20-Period Moving Average Confirmation")
    vol_fig = go.Figure()

    # Color bars: green if high volume, gray if below average
    bar_colors = ["#26a69a" if v > ma else "#b0bec5" for v, ma in zip(df["volume"], df["volume_ma"])]

    vol_fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["volume"],
            marker_color=bar_colors,
            name="15m Volume",
            opacity=0.8
        )
    )

    vol_fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["volume_ma"],
            mode="lines",
            line=dict(color="#ff9800", width=2, dash="dash"),
            name="20-Period Avg Volume"
        )
    )

    vol_fig.update_layout(
        height=260,
        xaxis_title="Timeline",
        yaxis_title="Volume",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(vol_fig, width="stretch")

st.markdown("---")

st.subheader(" RSI Indicator")

rsi_fig = go.Figure()

# RSI Line
rsi_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        mode="lines",
        name="RSI",
        line=dict(color="blue")
    )
)

# Overbought Line
rsi_fig.add_hline(
    y=70,
    line_dash="dash",
    line_color="red",
    annotation_text="Overbought (70)"
)

# Oversold Line
rsi_fig.add_hline(
    y=30,
    line_dash="dash",
    line_color="green",
    annotation_text="Oversold (30)"
)

rsi_fig.update_layout(
    height=350,
    template="plotly_white"
)

st.plotly_chart(rsi_fig, width="stretch")

st.markdown("---")

st.subheader("📈 Cumulative Equity Curve (Realized Returns)")

if len(trades) > 0:
    equity_df = pd.DataFrame(trades)
    equity_df["Trade_Num"] = range(1, len(equity_df) + 1)
    equity_df["Cumulative_Profit"] = equity_df["profit"].cumsum()

    eq_fig = go.Figure()

    eq_fig.add_trace(
        go.Scatter(
            x=equity_df["Trade_Num"],
            y=equity_df["Cumulative_Profit"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(38, 166, 154, 0.2)",
            line=dict(color="#00897b", width=3),
            marker=dict(size=9, color="#004d40", symbol="circle"),
            name="Cumulative Profit",
            hovertemplate="Trade #%{x}<br>Cumulative P&L: ₹%{y:.2f}<extra></extra>"
        )
    )

    eq_fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even (₹0)")

    eq_fig.update_layout(
        height=360,
        xaxis_title="Trade Sequence Number",
        yaxis_title="Realized Profit / Loss (₹)",
        template="plotly_white"
    )

    st.plotly_chart(eq_fig, width="stretch")
else:
    st.info("No completed trade cycles in current backtest.")
st.markdown("---")

# --------------------------------------------------
# Trade History & SQLite Database
# --------------------------------------------------

st.subheader(" Trade History (Current Backtest)")

if len(trades) > 0:
    trade_df = pd.DataFrame(trades)
    st.dataframe(trade_df, width="stretch")
else:
    st.warning("No trades found in current backtest.")

st.markdown("---")

with st.expander("📁 View Persisted SQLite Database Records (trading_data.db)"):
    try:
        db_records = load_trades()
        if db_records:
            db_df = pd.DataFrame(
                db_records,
                columns=["Trade ID", "Buy Price (₹)", "Sell Price (₹)", "Profit / Loss (₹)", "Timestamp"]
            )
            st.write(f"Total Logged Trades in SQLite: **{len(db_df)}**")
            st.dataframe(db_df.tail(50), width="stretch")
        else:
            st.info("No records currently stored in SQLite database.")
    except Exception as e:
        st.error(f"Error reading SQLite database: {e}")