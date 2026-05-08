import streamlit as st
import plotly.express as px
import pandas as pd

from utils.database import fetch_data
from utils.analytics import detect_anomaly

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Analytics",
    layout="wide"
)

# --------------------------------
# LOAD CSS
# --------------------------------
with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------------
# TITLE
# --------------------------------
st.title("📊 Advanced Analytics Dashboard")

# --------------------------------
# LOAD DATA
# --------------------------------
df = fetch_data()

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract hour
df["hour"] = df["timestamp"].dt.hour

# --------------------------------
# BASIC METRICS
# --------------------------------
avg_usage = round(df["usage_kwh"].mean(), 2)

max_usage = round(df["usage_kwh"].max(), 2)

min_usage = round(df["usage_kwh"].min(), 2)

peak_hour = df.groupby("hour")["usage_kwh"].mean().idxmax()

# --------------------------------
# METRICS
# --------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Usage", avg_usage)

col2.metric("Maximum Usage", max_usage)

col3.metric("Minimum Usage", min_usage)

col4.metric("Peak Hour", f"{peak_hour}:00")

st.markdown("---")

# --------------------------------
# HOURLY USAGE ANALYSIS
# --------------------------------
st.subheader("⏰ Hourly Usage Analysis")

hourly_usage = df.groupby("hour")["usage_kwh"].mean().reset_index()

fig1 = px.bar(
    hourly_usage,
    x="hour",
    y="usage_kwh",
    title="Average Hourly Electricity Usage"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------
# VOLTAGE TREND
# --------------------------------
st.subheader("⚡ Voltage Trend")

fig2 = px.line(
    df,
    x="timestamp",
    y="voltage",
    title="Voltage Over Time"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------
# CURRENT TREND
# --------------------------------
st.subheader("🔌 Current Trend")

fig3 = px.line(
    df,
    x="timestamp",
    y="current",
    title="Current Over Time"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------
# USAGE DISTRIBUTION
# --------------------------------
st.subheader("📈 Usage Distribution")

fig4 = px.histogram(
    df,
    x="usage_kwh",
    nbins=20,
    title="Electricity Usage Distribution"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------
# ANOMALY DETECTION
# --------------------------------
st.subheader("🚨 Anomaly Analysis")

df["status"] = df.apply(
    lambda row: detect_anomaly(
        row["usage_kwh"],
        row["voltage"],
        row["current"]
    ),
    axis=1
)

anomalies = df[df["status"].str.contains("Anomaly")]

st.write(f"Total Anomalies Detected: {len(anomalies)}")

fig5 = px.scatter(
    df,
    x="voltage",
    y="usage_kwh",
    color="status",
    title="Anomaly Detection Visualization"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# --------------------------------
# AI INSIGHTS
# --------------------------------
st.subheader("🤖 AI Insights")

if avg_usage > 4:
    st.warning(
        "High average electricity consumption detected."
    )

else:
    st.success(
        "Electricity consumption appears normal."
    )

if len(anomalies) > 5:
    st.error(
        "Frequent anomalies detected in the system."
    )

else:
    st.info(
        "System anomaly levels are stable."
    )
# --------------------------------
# EXPORT ANALYTICS DATA
# --------------------------------
st.markdown("---")

st.subheader("📥 Export Analytics Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Analytics Report",
    data=csv,
    file_name="powernova_analytics.csv",
    mime="text/csv"
)