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
    layout="wide"
)

st.sidebar.markdown("""
### ⚡ PowerNova AI
""")

st.sidebar.caption("AI Smart Energy Monitoring")
# --------------------------------
# LOAD CSS
# --------------------------------
with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

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
st.markdown("""
<div style='padding-top:10px;'>

<h1 style='font-size:52px;'>

🔮 AI Energy Predictions

</h1>

<p style='font-size:20px; color:#94a3b8;'>

Machine learning powered electricity forecasting and intelligent energy analysis.

</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------
# METRICS
# --------------------------------
st.markdown("## ⚡ Prediction Insights")

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

# --------------------------------
# AI MODEL INFO
# --------------------------------
st.markdown("---")

col1, col2 = st.columns([1,2])

with col1:

    st.markdown("## 🤖 AI Model")

    st.success("Linear Regression")

with col2:

    st.info("""
The forecasting model analyzes voltage,
current, and historical electricity usage
patterns to estimate future energy consumption.
""")

# --------------------------------
# TREND CHART
# --------------------------------
st.markdown("---")

st.subheader("📈 Recent Usage Trend")

chart_data = df.tail(10)

fig = px.line(
    chart_data,
    x="timestamp",
    y="usage_kwh",
    markers=True,
    title="Electricity Usage Forecast Trend"
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

    xaxis_title="Time",

    yaxis_title="Usage (kWh)",

    title_font=dict(size=22),

    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# AI EXPLANATION
# --------------------------------
st.markdown("---")

st.markdown("## 📘 How Prediction Works")

st.markdown("""
The AI forecasting model uses:

- Voltage readings
- Current readings
- Historical electricity usage trends

The Linear Regression algorithm learns electricity
consumption behavior and predicts future energy usage
based on real-time electrical patterns.
""")

# --------------------------------
# FUTURE ENHANCEMENTS
# --------------------------------
st.markdown("---")

st.markdown("## 🔮 Future Enhancements")

st.markdown("""
- Real IoT smart meter integration
- Deep learning forecasting models
- AI energy optimization
- Smart electricity alerts
- Cloud analytics platform
""")