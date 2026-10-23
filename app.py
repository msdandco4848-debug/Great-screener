
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Great Screen",
    page_icon="📈",
    layout="wide"
)

st.title("📈 GREAT SCREEN")
st.subheader("Indian Stock Market Screener")
st.write("Find companies that match your fundamental criteria.")

st.sidebar.header("Multibagger Filters")

min_roe = st.sidebar.slider("Minimum ROE (%)", 0, 50, 18)
min_roce = st.sidebar.slider("Minimum ROCE (%)", 0, 50, 20)
max_debt = st.sidebar.slider("Maximum Debt/Equity", 0.0, 2.0, 0.5)
min_sales = st.sidebar.slider("Minimum 3Y Sales Growth (%)", 0, 50, 15)
min_profit = st.sidebar.slider("Minimum 3Y Profit Growth (%)", 0, 50, 15)

data = {
    "Company": ["Demo Company"],
    "Market Cap (Cr)": [1500],
    "ROE (%)": [22],
    "ROCE (%)": [25],
    "Debt/Equity": [0.3],
    "Sales Growth 3Y (%)": [18],
    "Profit Growth 3Y (%)": [20],
    "Promoter Holding (%)": [60],
    "Pledged (%)": [0]
}

df = pd.DataFrame(data)

result = df[
    (df["ROE (%)"] > min_roe) &
    (df["ROCE (%)"] > min_roce) &
    (df["Debt/Equity"] < max_debt) &
    (df["Sales Growth 3Y (%)"] > min_sales) &
    (df["Profit Growth 3Y (%)"] > min_profit) &
    (df["Promoter Holding (%)"] > 50) &
    (df["Pledged (%)"] == 0)
]

st.subheader("Screening Results")
st.caption("Demo data only — not real market data.")
st.dataframe(result, use_container_width=True)

st.write("Companies matching your filters:", len(result))
