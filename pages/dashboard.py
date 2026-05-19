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
    page_title="PowerNova AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown("""
<style>

/* Main background */
.main {
    background-color: #0f172a;
}

/* Reduce top padding */
.block-container {
    padding-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1e293b;
    text-align: center;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.markdown("## ⚡ PowerNova AI")
st.sidebar.caption("AI Smart Energy Monitoring")

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
# DATABASE
# --------------------------------
create_table()

new_data = generate_live_data()

insert_data(new_data)

df = fetch_data()

latest = df.iloc[-1]

usage = latest["usage_kwh"]
voltage = latest["voltage"]
current = latest["current"]

prediction = predict_usage(
    voltage,
    current
)

anomaly = detect_anomaly(
    usage,
    voltage,
    current
)

# --------------------------------
# SIDEBAR SYSTEM INFO
# --------------------------------
st.sidebar.markdown("---")

st.sidebar.subheader("⚡ System Overview")

st.sidebar.success("AI System Active")

st.sidebar.metric(
    "Live Usage",
    f"{usage:.2f} kWh"
)

st.sidebar.metric(
    "Voltage",
    f"{voltage:.1f} V"
)

st.sidebar.metric(
    "Current",
    f"{current:.1f} A"
)

st.sidebar.markdown("---")

st.sidebar.success("All systems operating normally")

# --------------------------------
# HEADER
# --------------------------------
st.markdown("## ⚡ Smart Energy Dashboard")

st.caption(
    "Real-time electricity monitoring and AI-powered analytics."
)

st.markdown("---")

# --------------------------------
# METRICS
# --------------------------------
st.markdown("### ⚡ Live System Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Usage",
        f"{usage:.2f} kWh"
    )

with col2:
    st.metric(
        "Voltage",
        f"{voltage:.1f} V"
    )

with col3:
    st.metric(
        "Current",
        f"{current:.1f} A"
    )

with col4:
    st.metric(
        "AI Prediction",
        f"{prediction:.2f} kWh"
    )

st.markdown("---")

# --------------------------------
# CHART + AI STATUS
# --------------------------------
left, right = st.columns([2, 1])

# -------- LEFT SIDE GRAPH --------
with left:

    st.subheader("📈 Live Electricity Usage")

    chart_data = df.tail(20).copy()

    chart_data["timestamp"] = pd.to_datetime(
        chart_data["timestamp"]
    )

    chart_data["time"] = chart_data[
        "timestamp"
    ].dt.strftime("%H:%M:%S")

    fig = px.line(
        chart_data,
        x="time",
        y="usage_kwh"
    )

    fig.update_traces(
        line_smoothing=0.5,
        mode="lines",
        line=dict(
            width=4,
            shape="spline"
        )
    )

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        font_color="white",

        height=320,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
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

# -------- RIGHT SIDE STATUS --------
with right:

    st.subheader("🚨 AI Monitoring")

    if anomaly == -1:
        st.error(
            "Abnormal electricity pattern detected"
        )

    else:
        st.success(
            "System operating normally"
        )

    st.info("""
AI anomaly detection continuously monitors:

• Electricity usage  
• Voltage levels  
• Current fluctuations  

to identify unusual patterns in real time.
""")

st.markdown("---")

# --------------------------------
# TABLE + ACTIONS
# --------------------------------
left, right = st.columns([2, 1])

# -------- TABLE --------
with left:

    st.subheader("📋 Recent Smart Meter Readings")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

# -------- ACTIONS --------
with right:

    st.subheader("⚡ Quick Actions")

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="electricity_data.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("")

    if st.button(
        "📄 Generate PDF Report",
        use_container_width=True
    ):

        pdf_file = generate_pdf_report(df)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="powernova_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )