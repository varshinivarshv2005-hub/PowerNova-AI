import streamlit as st
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

from utils.simulator import generate_data
from utils.database import create_table, insert_data, fetch_data
from utils.analytics import predict_usage, detect_anomaly

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)
# --------------------------------
# LOAD CUSTOM CSS
# --------------------------------
with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("⚙ Dashboard Settings")

refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)",
    1,
    10,
    3
)

# --------------------------------
# AUTO REFRESH
# --------------------------------
st_autorefresh(
    interval=refresh_rate * 1000,
    key="dashboard_refresh"
)

# --------------------------------
# DATABASE
# --------------------------------
create_table()

new_data = generate_data()

insert_data(new_data)

df = fetch_data()

# --------------------------------
# HEADER
# --------------------------------
st.title("⚡ Live Electricity Dashboard")

st.markdown("---")

# --------------------------------
# LATEST DATA
# --------------------------------
latest = df.iloc[-1]

predicted_usage = predict_usage(
    latest["voltage"],
    latest["current"]
)

anomaly_status = detect_anomaly(
    latest["usage_kwh"],
    latest["voltage"],
    latest["current"]
)

# --------------------------------
# METRICS
# --------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Usage (kWh)",
    latest["usage_kwh"]
)

col2.metric(
    "Voltage (V)",
    latest["voltage"]
)

col3.metric(
    "Current (A)",
    latest["current"]
)

col4.metric(
    "Predicted Usage",
    predicted_usage
)

st.markdown("---")

# --------------------------------
# SYSTEM STATUS
# --------------------------------
st.subheader("🚨 System Status")

if "Anomaly" in anomaly_status:

    st.error(anomaly_status)

else:

    st.success(anomaly_status)

# --------------------------------
# CHART
# --------------------------------
st.subheader("📈 Electricity Usage Trend")

fig = px.line(
    df,
    x="timestamp",
    y="usage_kwh",
    title="Electricity Consumption Over Time"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# RECENT READINGS
# --------------------------------
st.subheader("📋 Recent Readings")

st.dataframe(df.tail(10))
# --------------------------------
# CSV DOWNLOAD
# --------------------------------
st.markdown("---")

st.subheader("📥 Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Electricity Data",
    data=csv,
    file_name="powernova_data.csv",
    mime="text/csv"
)