import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import fetch_data


# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Analytics",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------
df = fetch_data()
df = df.tail(50)
# --------------------------------
# TITLE
# --------------------------------
st.title("📊 Electricity Analytics")

st.markdown("---")

# --------------------------------
# BASIC STATS
# --------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Usage",
    round(df["usage_kwh"].mean(), 2)
)

col2.metric(
    "Maximum Usage",
    round(df["usage_kwh"].max(), 2)
)

col3.metric(
    "Minimum Usage",
    round(df["usage_kwh"].min(), 2)
)

# --------------------------------
# USAGE TREND
# --------------------------------
st.markdown("---")

st.subheader("📈 Usage Trend Analysis")

trend_data = df.tail(100)

fig1 = px.line(
    trend_data,
    x="timestamp",
    y="usage_kwh",
    markers=True,
    title="Electricity Usage Trend"
)

fig1.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    transition_duration=500
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="analytics_trend"
)

# --------------------------------
# VOLTAGE ANALYSIS
# --------------------------------
st.markdown("---")

st.subheader("⚡ Voltage Analysis")

fig2 = px.line(
    trend_data,
    x="timestamp",
    y="voltage",
    title="Voltage Fluctuation"
)

fig2.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="analytics_voltage"
)

# --------------------------------
# CURRENT ANALYSIS
# --------------------------------
st.markdown("---")

st.subheader("🔌 Current Analysis")

fig3 = px.line(
    trend_data,
    x="timestamp",
    y="current",
    title="Current Variation"
)

fig3.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="analytics_current"
)

# --------------------------------
# CORRELATION
# --------------------------------
st.markdown("---")

st.subheader("🧠 Feature Correlation")

corr = df[[
    "usage_kwh",
    "voltage",
    "current"
]].corr()

fig4 = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Matrix"
)

fig4.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="analytics_corr"
)