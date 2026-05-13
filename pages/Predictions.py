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
st.title("🔮 AI Predictions")

st.markdown("---")

# --------------------------------
# MAIN METRICS
# --------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Predicted Usage (kWh)",
    round(predicted_usage, 2)
)

col2.metric(
    "Current Voltage",
    round(latest["voltage"], 2)
)

col3.metric(
    "Current (A)",
    round(latest["current"], 2)
)

# --------------------------------
# MODEL INFO
# --------------------------------
st.info(
    "Prediction generated using Linear Regression model trained on electricity usage patterns."
)

# --------------------------------
# PREDICTION EXPLANATION
# --------------------------------
st.markdown("""
## 📘 How Prediction Works

The AI model analyzes:

- Voltage values
- Current values
- Previous electricity usage trends

Using Linear Regression, the model predicts future electricity consumption based on current electrical behavior.
""")

# --------------------------------
# RECENT USAGE TREND
# --------------------------------
st.markdown("---")

st.subheader("📈 Recent Usage Trend")

chart_data = df.tail(20)

fig = px.line(
    chart_data,
    x="timestamp",
    y="usage_kwh",
    markers=True
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Timestamp",
    yaxis_title="Usage (kWh)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# FUTURE SCOPE
# --------------------------------
st.markdown("---")

st.success(
    "Future versions can integrate IoT smart meters for real-time AI-based forecasting."
)