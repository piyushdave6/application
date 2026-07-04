import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Stock Price Viewer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Yahoo Finance Stock Chart")

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
)

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]
)

interval = st.selectbox(
    "Data Interval",
    [
        "1d",
        "1wk",
        "1mo"
    ]
)

if st.button("Fetch Data"):

    with st.spinner("Downloading data..."):

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True
        )

    if df.empty:
        st.error("No data found.")
    else:

        st.success("Data Downloaded Successfully")

        st.subheader("Latest Data")

        st.dataframe(df.tail())

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.update_layout(
            title=f"{ticker} Closing Price",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
            template="plotly_white",
            height=650
        )

        st.plotly_chart(fig, use_container_width=True)

        csv = df.to_csv().encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            file_name=f"{ticker}_{period}.csv",
            mime="text/csv"
        )
