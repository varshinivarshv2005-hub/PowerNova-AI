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

# --------------------------------
# HEADER
# --------------------------------
st.markdown("""
<div style='padding-top:10px;'>

<h1 style='font-size:52px;'>

📊 Energy Analytics

</h1>

<p style='font-size:20px; color:#94a3b8;'>

Analyze electricity usage trends and smart energy insights in real time.

</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------
# ANALYTICS METRICS
# --------------------------------
avg_usage = df["usage_kwh"].mean()
max_usage = df["usage_kwh"].max()
min_usage = df["usage_kwh"].min()
avg_voltage = df["voltage"].mean()

st.markdown("## ⚡ Usage Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Usage",
        f"{avg_usage:.2f} kWh"
    )

with col2:
    st.metric(
        "Maximum Usage",
        f"{max_usage:.2f} kWh"
    )

with col3:
    st.metric(
        "Minimum Usage",
        f"{min_usage:.2f} kWh"
    )

with col4:
    st.metric(
        "Average Voltage",
        f"{avg_voltage:.1f} V"
    )

# --------------------------------
# USAGE TREND GRAPH
# --------------------------------
st.markdown("---")

st.subheader("📈 Electricity Usage Trend")

chart_data = df.tail(15)

fig = px.line(
    chart_data,
    x="timestamp",
    y="usage_kwh",
    markers=True,
    title="Smart Energy Consumption Trend"
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
# VOLTAGE ANALYSIS
# --------------------------------
st.markdown("---")

st.subheader("⚡ Voltage Analysis")

voltage_fig = px.area(
    chart_data,
    x="timestamp",
    y="voltage",
    title="Voltage Monitoring"
)

voltage_fig.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450
)

st.plotly_chart(
    voltage_fig,
    use_container_width=True
)

# --------------------------------
# SMART INSIGHTS
# --------------------------------
st.markdown("---")

st.markdown("## 🤖 Smart Energy Insights")

if avg_usage > 6:

    st.warning("""
Electricity usage is currently higher than normal.
Energy optimization may help reduce consumption.
""")

else:

    st.success("""
Electricity consumption is currently operating
within a stable and efficient range.
""")

# --------------------------------
# DATA TABLE
# --------------------------------
st.markdown("---")

st.markdown("## 📋 Electricity Data")

st.dataframe(
    df.tail(10),
    use_container_width=True
)

# --------------------------------
# FUTURE SCOPE
# --------------------------------
st.markdown("---")

st.markdown("## 🔮 Future Analytics Features")

st.markdown("""
- AI-powered consumption forecasting
- Real IoT smart meter integration
- Peak load analysis
- Energy optimization recommendations
- Cloud-based analytics dashboard
""")