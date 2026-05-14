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
    page_title="Dashboard",
    layout="wide"
)

st.sidebar.markdown("""
### ⚡ PowerNova AI
""")

st.sidebar.caption("AI Smart Energy Monitoring")
# --------------------------------
# LOAD CUSTOM CSS
# --------------------------------
with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------------
# SIDEBAR SETTINGS
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

# Generate new simulated reading
new_data = generate_live_data()

# Store reading in database
insert_data(new_data)

# Fetch database data
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
# SIDEBAR
# --------------------------------
st.sidebar.markdown("---")

st.sidebar.subheader("⚡ System Overview")

st.sidebar.success("AI System Active")

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

st.sidebar.info("""
PowerNova AI monitors electricity usage,
detects anomalies, and predicts future
energy consumption using AI models.
""")

st.sidebar.markdown("---")

st.sidebar.caption("PowerNova AI • Version 1.0")

# --------------------------------
# HEADER
# --------------------------------
st.markdown("""
<div style='padding-top:10px;'>

<h1 style='font-size:52px;'>

⚡ Smart Energy Dashboard

</h1>

<p style='font-size:20px; color:#94a3b8;'>

Real-time electricity monitoring and AI-powered analytics.

</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------
# METRICS
# --------------------------------
st.markdown("## ⚡ Live System Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Usage",
        f"{latest['usage_kwh']:.2f} kWh"
    )

with col2:
    st.metric(
        "Voltage",
        f"{latest['voltage']:.1f} V"
    )

with col3:
    st.metric(
        "Current",
        f"{latest['current']:.1f} A"
    )

with col4:
    st.metric(
        "AI Prediction",
        f"{predicted_usage:.2f} kWh"
    )

# --------------------------------
# SYSTEM STATUS
# --------------------------------
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:

    st.markdown("## 🚨 AI Monitoring Status")

    if anomaly == -1:
        st.error("⚠ Abnormal electricity pattern detected")

    else:
        st.success("✅ System operating normally")

with col2:

    st.info("""
AI anomaly detection continuously monitors voltage,
current, and electricity usage patterns in real time.
""")

# --------------------------------
# PROFESSIONAL LIVE CHART
# --------------------------------

chart_data = df.tail(15).copy()

chart_data["timestamp"] = pd.to_datetime(
    chart_data["timestamp"]
)

fig = px.line(
    chart_data,
    x="timestamp",
    y="usage_kwh",
    markers=True
)

fig.update_traces(
    mode="lines+markers",
    line=dict(
        width=4,
        shape="spline"
    ),
    marker=dict(
        size=8
    )
)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450,

    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    ),

    xaxis=dict(
        title="Time",
        showgrid=False
    ),

    yaxis=dict(
        title="Usage (kWh)",
        gridcolor="rgba(255,255,255,0.08)"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# RECENT READINGS
# --------------------------------
st.markdown("---")

st.markdown("## 📋 Recent Smart Meter Readings")

st.dataframe(
    df.tail(10),
    use_container_width=True
)

# --------------------------------
# CSV DOWNLOAD
# --------------------------------
st.markdown("---")

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