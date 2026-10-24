import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="GREAT SCREEN", layout="wide")
st.title("📈 GREAT SCREEN")
st.caption("Indian Stock Market Screener | Yahoo Finance data")

symbols = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "BEL": "BEL.NS",
    "COALINDIA": "COALINDIA.NS",
    "BLS": "BLS.NS",
    "KPITTECH": "KPITTECH.NS",
    "POLYCAB": "POLYCAB.NS",
    "WAAREERTL": "WAAREERTL.NS",
    "NEWGEN": "NEWGEN.NS",
    "ASHOKA": "ASHOKA.NS",
    "KIRLPNU": "KIRLPNU.NS",
    "EMMVEE": "EMMVEE.NS",
}

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock(symbol, ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "Stock": symbol,
            "Price": info.get("currentPrice"),
            "PE": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
            "ROE %": (
                info.get("returnOnEquity") * 100
                if info.get("returnOnEquity") is not None
                else None
            ),
            "Debt/Equity": (
                info.get("debtToEquity") / 100
                if info.get("debtToEquity") is not None
                else None
            ),
            "Sales Growth %": (
                info.get("revenueGrowth") * 100
                if info.get("revenueGrowth") is not None
                else None
            ),
            "Market Cap (Cr)": (
                info.get("marketCap") / 10000000
                if info.get("marketCap") is not None
                else None
            ),
        }
    except Exception:
        return {"Stock": symbol, "Error": "Data unavailable"}

st.sidebar.header("Screening Filters")
max_pe = st.sidebar.number_input("Maximum PE", 1, 500, 40)
min_roe = st.sidebar.number_input("Minimum ROE %", 0, 100, 18)
max_debt = st.sidebar.number_input("Maximum Debt/Equity", 0.0, 10.0, 0.5)
min_sales = st.sidebar.number_input("Minimum Sales Growth %", 0, 200, 15)

selected = st.multiselect(
    "Select NSE stocks",
    list(symbols.keys()),
    default=list(symbols.keys())[:5]
)

if st.button("🔍 Run Screener", type="primary"):
    if not selected:
        st.warning("Select at least one stock.")
    else:
        rows = []
        progress = st.progress(0)

        for i, name in enumerate(selected):
            rows.append(get_stock(name, symbols[name]))
            progress.progress((i + 1) / len(selected))

        df = pd.DataFrame(rows)
        progress.empty()

        if "Error" in df.columns:
            st.warning("Some stocks may not have available data.")

        st.subheader("Stock Results")
        st.dataframe(df, use_container_width=True, hide_index=True)

        if "ROE %" in df.columns:
            valid = df.dropna(
                subset=["PE", "ROE %", "Debt/Equity", "Sales Growth %"]
            )
            filtered = valid[
                (valid["PE"] > 0)
                & (valid["PE"] <= max_pe)
                & (valid["ROE %"] >= min_roe)
                & (valid["Debt/Equity"] <= max_debt)
                & (valid["Sales Growth %"] >= min_sales)
            ]
            st.subheader("⭐ Matching Quality Stocks")
            st.dataframe(
                filtered, use_container_width=True, hide_index=True
            )
            st.caption(
                "Filters are screening criteria, not investment advice."
            )

        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "great_screen.csv",
            "text/csv"
        )

st.info(
    "Yahoo Finance data may be delayed, incomplete or unavailable. "
    "This is not an official NSE real-time data feed."
)
