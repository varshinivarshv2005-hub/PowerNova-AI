import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

from utils.simulator import generate_live_data

from utils.database import (
    create_table,
    insert_data,
    fetch_data
)

from utils.analytics import (
    predict_usage,
    detect_anomaly
)

from utils.report_generator import generate_pdf_report


# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="PowerNova AI",
    layout="wide"
)

# --------------------------------
# SIDEBAR
# --------------------------------
refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)",
    1,
    10,
    3
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key="dashboard_refresh"
)

# --------------------------------
# DATABASE SETUP
# --------------------------------
create_table()

# Generate simulated live data
new_data = generate_live_data()

# Store data in database
insert_data(new_data)

# Fetch all stored data
df = fetch_data()

# --------------------------------
# LATEST DATA
# --------------------------------
latest = df.iloc[-1]

predicted_usage = predict_usage(
    latest["voltage"],
    latest["current"]
)

anomaly = detect_anomaly(
    latest["usage_kwh"],
    latest["voltage"],
    latest["current"]
)

# --------------------------------
# SIDEBAR SYSTEM INFO
# --------------------------------
st.sidebar.markdown("---")

st.sidebar.subheader("⚡ System Info")

st.sidebar.success("System Active")

st.sidebar.metric(
    "Live Usage",
    f"{latest['usage_kwh']:.2f} kWh"
)

st.sidebar.metric(
    "Voltage",
    f"{latest['voltage']:.1f} V"
)

st.sidebar.metric(
    "Current",
    f"{latest['current']:.1f} A"
)

st.sidebar.markdown("---")

st.sidebar.caption("PowerNova AI v1.0")

# --------------------------------
# HEADER
# --------------------------------
st.title("⚡ Live Electricity Dashboard")

st.markdown("---")

# --------------------------------
# METRICS
# --------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Usage (kWh)",
    round(latest["usage_kwh"], 2)
)

col2.metric(
    "Voltage (V)",
    round(latest["voltage"], 2)
)

col3.metric(
    "Current (A)",
    round(latest["current"], 2)
)

col4.metric(
    "Predicted Usage",
    round(predicted_usage, 2)
)

# --------------------------------
# SYSTEM STATUS
# --------------------------------
st.markdown("---")

st.subheader("🚨 System Status")

if anomaly == -1:
    st.error("⚠️ Anomaly Detected")
else:
    st.success("✅ Normal")

# --------------------------------
# LIVE CHART
# --------------------------------
st.markdown("---")

st.subheader("📈 Live Electricity Usage")

chart_data = df.tail(20)
chart_data = chart_data.sort_values("timestamp")

fig = px.line(
    chart_data,
    x="timestamp",
    y="usage_kwh",
    markers=True,
    title="Electricity Usage Trend"
)

fig.update_traces(
    line=dict(width=3)
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Timestamp",
    yaxis_title="Usage (kWh)",
    transition_duration=500
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="dashboard_chart"
)

# --------------------------------
# RECENT READINGS
# --------------------------------
st.markdown("---")

st.subheader("📋 Recent Readings")

st.dataframe(
    df.tail(10),
    use_container_width=True
)

# --------------------------------
# CSV DOWNLOAD
# --------------------------------
csv = df.to_csv(index=False)

st.download_button(
    label="⬇ Download CSV Data",
    data=csv,
    file_name="electricity_data.csv",
    mime="text/csv"
)

# --------------------------------
# PDF REPORT
# --------------------------------
st.markdown("---")

st.subheader("📄 Generate PDF Report")

if st.button("Generate PDF Report"):

    pdf_file = generate_pdf_report(df)

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="powernova_report.pdf",
            mime="application/pdf"
        )