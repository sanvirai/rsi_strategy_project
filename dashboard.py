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
stock = st.sidebar.selectbox(
    "Select Stock",
    [
        "HDFCBANK.NS",
        "RELIANCE.NS",
        "INFY.NS",
        "TCS.NS",
        "ITC.NS",
        "KOTAKBANK.NS"
    ]
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_live_data(symbol=stock)

if "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")

elif "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")

else:
    st.write(df.columns)
    st.error("Date column not found.")
    st.stop()
# --------------------------------------------------
# Load Live Data
# --------------------------------------------------

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

    st.subheader(" Maximum Drawdown Comparison")
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

        

        matrix_data = [
            [cm[0][0], cm[0][1]],  # FN, TP
            [cm[1][0], cm[1][1]]   # TN, FP
        ]

        cell_labels = [
            [
                f"FN: {cm[1][0]}",
                f"TP: {cm[1][1]}"
            ],
            [
                f"TN: {cm[0][0]}",
                f"FP: {cm[0][1]}"
            ]
        ]
        cell_labels = [
        [f"TN: {cm[0][0]}", f"FP: {cm[0][1]}"],
        [f"FN: {cm[1][0]}", f"TP: {cm[1][1]}"]
    ]
        fig = go.Figure(
            data=go.Heatmap(
                z=matrix_data,

                x=[
                    "Predicted: No Buy (0)",
                    "Predicted: Buy (1)"
                ],

                y=[
                    "Actual: No Price Up (0)",
                    "Actual: Price Up (1)"
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

     st.subheader(" Volume Analysis")

     st.write(f"Current Volume: {int(df['volume'].iloc[-1])}")
     st.write(f"20-Period Avg Volume: {int(df['volume_ma'].iloc[-1])}")

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

# Buy Signals
fig.add_trace(
    go.Scatter(
        x=df[df["buy_signal"]].index,
        y=df[df["buy_signal"]]["low"],
        mode="markers",
        marker=dict(
            symbol="triangle-up",
            size=12,
            color="green"
        ),
        name="Buy"
    )
)

# Sell Signals
fig.add_trace(
    go.Scatter(
        x=df[df["sell_signal"]].index,
        y=df[df["sell_signal"]]["high"],
        mode="markers",
        marker=dict(
            symbol="triangle-down",
            size=12,
            color="red"
        ),
        name="Sell"
    )
)

fig.update_layout(
    height=600,
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False,
    template="plotly_white"
)

st.plotly_chart(fig, width="stretch")

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

st.subheader(" Equity Curve")

if len(trades) > 0:
    equity = pd.DataFrame(trades)
    equity["Equity"] = equity["profit"].cumsum()
    st.line_chart(equity["Equity"])
else:
    st.info("No equity data available.")
st.markdown("---")

# --------------------------------------------------
# Trade History
# --------------------------------------------------

st.subheader(" Trade History")

if len(trades) > 0:
    trade_df = pd.DataFrame(trades)
    st.dataframe(trade_df, width="stretch")
else:
    st.warning("No trades found.")