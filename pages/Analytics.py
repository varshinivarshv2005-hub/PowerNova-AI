import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import fetch_data

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Analytics",
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

st.sidebar.success("Analytics System Active")

# --------------------------------
# LOAD DATA
# --------------------------------
df = fetch_data()

# --------------------------------
# HEADER
# --------------------------------
st.markdown("## 📊 Energy Analytics")

st.caption(
    "Analyze electricity usage trends and smart energy insights in real time."
)

st.markdown("---")

# --------------------------------
# ANALYTICS METRICS
# --------------------------------
avg_usage = df["usage_kwh"].mean()
max_usage = df["usage_kwh"].max()
min_usage = df["usage_kwh"].min()
avg_voltage = df["voltage"].mean()

st.markdown("### ⚡ Usage Statistics")

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

st.markdown("---")

# --------------------------------
# USAGE TREND GRAPH
# --------------------------------
st.subheader("📈 Electricity Usage Trend")

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
# VOLTAGE ANALYSIS
# --------------------------------
st.subheader("⚡ Voltage Analysis")

voltage_fig = px.area(
    chart_data,
    x="time",
    y="voltage"
)

voltage_fig.update_layout(

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
        title="Voltage",
        gridcolor="rgba(255,255,255,0.08)"
    )
)

st.plotly_chart(
    voltage_fig,
    use_container_width=True
)

st.markdown("---")

# --------------------------------
# SMART INSIGHTS
# --------------------------------
st.subheader("🤖 Smart Energy Insights")

if avg_usage > 6:

    st.warning("""
Electricity usage is currently higher than normal.

Energy optimization may help reduce consumption.
""")

else:

    st.success("""
Electricity consumption is operating within a stable and efficient range.
""")

st.markdown("---")

# --------------------------------
# DATA TABLE
# --------------------------------
st.subheader("📋 Recent Electricity Data")

display_df = df.tail(10).copy()

st.dataframe(
    display_df,
    use_container_width=True,
    height=350
)

st.markdown("---")

# --------------------------------
# FUTURE FEATURES
# --------------------------------
st.subheader("🔮 Future Analytics Features")

st.info("""
• AI-powered consumption forecasting  
• Real IoT smart meter integration  
• Peak load analysis  
• Energy optimization recommendations  
• Cloud-based analytics dashboard
""")