
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Great Screen",
    page_icon="📈",
    layout="wide"
)

st.title("📈 GREAT SCREEN")
st.subheader("Indian Stock Market Screener")
st.caption("Fundamental screening tool | CSV data only — not live market data")

# Expected CSV columns
columns = [
    "Company",
    "Symbol",
    "Market Cap (Cr)",
    "ROE (%)",
    "ROCE (%)",
    "Debt/Equity",
    "Sales Growth 3Y (%)",
    "Profit Growth 3Y (%)",
    "Operating Margin (%)",
    "Promoter Holding (%)",
    "Pledged (%)",
    "PEG Ratio",
    "PE",
    "Industry PE",
    "Price (₹)"
]

# Example data is fictional
demo_data = [
    ["Demo Alpha", "DEMO1", 1500, 22, 25, 0.30, 18, 20, 17, 60, 0, 0.8, 18, 25, 100],
    ["Demo Beta", "DEMO2", 3500, 25, 29, 0.20, 22, 24, 19, 65, 0, 0.9, 20, 28, 250],
    ["Demo Gamma", "DEMO3", 900, 19, 23, 0.40, 17, 18, 16, 55, 0, 0.7, 22, 24, 80],
    ["Demo Delta", "DEMO4", 7000, 16, 18, 0.80, 12, 14, 12, 48, 2, 1.4, 30, 25, 400],
]

demo_df = pd.DataFrame(demo_data, columns=columns)

st.info(
    "Demo companies are fictional. Upload your own CSV to screen "
    "actual stock data. Results depend on the data you provide."
)

template_df = pd.DataFrame(columns=columns)

st.download_button(
    "⬇️ Download CSV Template",
    data=template_df.to_csv(index=False).encode("utf-8"),
    file_name="great_screen_template.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader(
    "📂 Upload your stock data CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        missing = [col for col in columns if col not in df.columns]

        if missing:
            st.error("CSV-ல் இந்த columns இல்லை: " + ", ".join(missing))
            st.write("மேலே உள்ள CSV Template-ஐ download செய்து அதே column names பயன்படுத்துங்கள்.")
            st.stop()

        data_source = "Uploaded CSV"
    except Exception as e:
        st.error(f"CSV file-ஐ படிக்க முடியவில்லை: {e}")
        st.stop()
else:
    df = demo_df.copy()
    data_source = "Fictional Demo Data"

# Convert screening columns to numeric
numeric_columns = [c for c in columns if c not in ["Company", "Symbol"]]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

st.caption(f"Data source: {data_source} | Rows: {len(df)}")

st.sidebar.header("🔎 Multibagger Filters")

min_market_cap = st.sidebar.number_input(
    "Minimum Market Cap (Cr)", min_value=0, value=500, step=100
)
max_market_cap = st.sidebar.number_input(
    "Maximum Market Cap (Cr)", min_value=500, value=20000, step=500
)
min_roe = st.sidebar.slider("Minimum ROE (%)", 0, 50, 18)
min_roce = st.sidebar.slider("Minimum ROCE (%)", 0, 50, 20)
max_debt = st.sidebar.slider("Maximum Debt/Equity", 0.0, 2.0, 0.5, 0.1)
min_sales = st.sidebar.slider("Minimum 3Y Sales Growth (%)", 0, 50, 15)
min_profit = st.sidebar.slider("Minimum 3Y Profit Growth (%)", 0, 50, 15)
min_margin = st.sidebar.slider("Minimum Operating Margin (%)", 0, 50, 15)
min_promoter = st.sidebar.slider("Minimum Promoter Holding (%)", 0, 100, 50)
max_pledged = st.sidebar.number_input(
    "Maximum Pledged (%)", min_value=0.0, value=0.0, step=0.5
)
max_peg = st.sidebar.number_input(
    "Maximum PEG Ratio", min_value=0.0, value=1.0, step=0.1
)
pe_below_industry = st.sidebar.checkbox(
    "PE below Industry PE", value=True
)

# Apply filters
result = df[
    df["Market Cap (Cr)"].between(min_market_cap, max_market_cap)
    & (df["ROE (%)"] >= min_roe)
    & (df["ROCE (%)"] >= min_roce)
    & (df["Debt/Equity"] <= max_debt)
    & (df["Sales Growth 3Y (%)"] >= min_sales)
    & (df["Profit Growth 3Y (%)"] >= min_profit)
    & (df["Operating Margin (%)"] >= min_margin)
    & (df["Promoter Holding (%)"] >= min_promoter)
    & (df["Pledged (%)"] <= max_pledged)
    & (df["PEG Ratio"] <= max_peg)
].copy()

if pe_below_industry:
    result = result[result["PE"] < result["Industry PE"]]

st.subheader("📊 Screening Results")

a, b, c = st.columns(3)
a.metric("Stocks Matching", len(result))
b.metric("Stocks in Dataset", len(df))
c.metric("Data Source", data_source)

if result.empty:
    st.warning("இந்த filters-க்கு பொருந்தும் stocks இல்லை. Filter values-ஐ மாற்றிப் பாருங்கள்.")
else:
    st.dataframe(result, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download Filtered Results",
        data=result.to_csv(index=False).encode("utf-8"),
        file_name="great_screen_results.csv",
        mime="text/csv"
    )

st.divider()
st.caption(
    "Educational screening tool only. Filters do not guarantee multibagger returns. "
    "Verify financial data and do your own research before investing."
)

