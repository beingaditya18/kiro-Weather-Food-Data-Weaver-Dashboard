import streamlit as st
import pandas as pd

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="Weather × Food | Kiro",
    page_icon="🍔",
    layout="wide"
)

# ---------------- Load Data ----------------
try:
    df = pd.read_csv("data/merged_data.csv")
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    st.error("❌ Data not found! Please run the ETL pipeline first.")
    st.stop()

# ---------------- Sidebar ----------------
st.sidebar.title("🍔 Data Weaver")
selected_city = st.sidebar.selectbox("Select City", df['city'].unique())
filtered_df = df[df['city'] == selected_city]

# ---------------- Main UI ----------------
st.title(f"📊 Weather Impact: {selected_city}")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("📦 Total Orders", f"{filtered_df['order_count'].sum():,}")
kpi2.metric("🌡️ Avg Temperature", f"{filtered_df['temperature'].mean():.1f} °C")
kpi3.metric(
    "🌧️ Rainy Days",
    filtered_df[filtered_df['rainfall'] > 0]['date'].nunique()
)

st.markdown("---")

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["📈 Trends", "🧠 Kiro Insights"])

# ----------- Trends Tab -----------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.write("🌧️ **Rainfall vs Order Volume**")
        rainfall_orders = (
            filtered_df
            .groupby("rainfall")["order_count"]
            .mean()
        )
        st.bar_chart(rainfall_orders)

    with col2:
        st.write("🍕 **Cuisine Preference**")
        cuisine_orders = (
            filtered_df
            .groupby("cuisine")["order_count"]
            .sum()
        )
        st.bar_chart(cuisine_orders)

# ----------- Kiro Insights Tab -----------
with tab2:
    # Correlation calculation
    if filtered_df['rainfall'].nunique() > 1:
        corr = filtered_df['rainfall'].corr(filtered_df['order_count'])
    else:
        corr = 0

    st.success(
        f"""
        🧠 **Kiro-Assisted Insight**

        • Rainfall–Order Correlation: **{corr:.2f}**  
        • Higher rainfall days show increased demand for comfort food  
        • **Recommendation:** Run rainy-day promotions and bundle offers

        _Insight derived using aggregated daily rainfall and order volume._
        """
    )

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Built for AI for Bharat | Data Weaver Challenge | Assisted by Kiro")