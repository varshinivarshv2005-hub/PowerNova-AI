import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import fetch_data
from utils.analytics import predict_usage

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Predictions",
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

/* Reduce top spacing */
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

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.markdown("## ⚡ PowerNova AI")
st.sidebar.caption("AI Smart Energy Monitoring")

st.sidebar.markdown("---")

st.sidebar.success("Prediction System Active")

# --------------------------------
# LOAD DATA
# --------------------------------
df = fetch_data()

latest = df.iloc[-1]

predicted_usage = predict_usage(
    latest["voltage"],
    latest["current"]
)

# --------------------------------
# HEADER
# --------------------------------
st.markdown("## 🔮 AI Energy Predictions")

st.caption(
    "Machine learning powered electricity forecasting and intelligent energy analysis."
)

st.markdown("---")

# --------------------------------
# METRICS
# --------------------------------
st.markdown("### ⚡ Prediction Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Predicted Usage",
        f"{predicted_usage:.2f} kWh"
    )

with col2:
    st.metric(
        "Current Voltage",
        f"{latest['voltage']:.1f} V"
    )

with col3:
    st.metric(
        "Current",
        f"{latest['current']:.1f} A"
    )

st.markdown("---")

# --------------------------------
# AI MODEL SECTION
# --------------------------------
left, right = st.columns([1, 2])

with left:

    st.subheader("🤖 AI Model")

    st.success("Linear Regression")

with right:

    st.info("""
The forecasting model analyzes:

• Voltage readings  
• Current readings  
• Historical electricity usage patterns  

to estimate future energy consumption.
""")

st.markdown("---")

# --------------------------------
# FORECAST GRAPH
# --------------------------------
st.subheader("📈 Electricity Usage Forecast Trend")

chart_data = df.tail(15).copy()

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

st.markdown("---")

# --------------------------------
# HOW PREDICTION WORKS
# --------------------------------
left, right = st.columns([2, 1])

with left:

    st.subheader("📘 How Prediction Works")

    st.markdown("""
The prediction system uses:

- Voltage readings
- Current readings
- Historical electricity usage patterns

The Linear Regression model learns relationships
between electrical parameters and predicts future
electricity consumption.
""")

with right:

    st.subheader("⚡ AI Insight")

    st.success(
        "Electricity usage prediction operating normally."
    )

st.markdown("---")

# --------------------------------
# FUTURE ENHANCEMENTS
# --------------------------------
st.subheader("🔮 Future Enhancements")

st.info("""
• Real IoT smart meter integration  
• Deep learning forecasting models  
• AI energy optimization  
• Smart electricity alerts  
• Cloud analytics platform
""")