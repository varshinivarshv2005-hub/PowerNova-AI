import streamlit as st
from datetime import datetime

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="PowerNova AI",
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
# HERO SECTION
# --------------------------------
st.title("⚡ PowerNova AI")

st.subheader(
    "AI-Powered Smart Electricity Analytics Platform"
)

st.markdown("---")

# --------------------------------
# SYSTEM STATUS
# --------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "System Status",
    "Online"
)

col2.metric(
    "AI Models",
    "Active"
)

current_time = datetime.now().strftime("%H:%M:%S")

col3.metric(
    "Current Time",
    current_time
)

st.markdown("---")

# --------------------------------
# PROJECT OVERVIEW
# --------------------------------
st.markdown("""
## 🚀 Project Overview

PowerNova AI is an intelligent electricity analytics platform inspired by modern smart energy systems.

The platform simulates real smart meter behavior and applies machine learning algorithms for:

- Smart electricity monitoring
- AI-based forecasting
- Anomaly detection
- Real-time analytics
- Energy consumption insights

---

## 🤖 AI Features

### 📈 Forecasting
Predicts future electricity usage using:
- Linear Regression

### 🚨 Anomaly Detection
Detects abnormal electricity patterns using:
- Isolation Forest

---

## 🛠 Technologies Used

- Python
- Streamlit
- SQLite
- Plotly
- Scikit-learn
- Pandas

---

## 📊 Key Features

✅ Live electricity simulation  
✅ AI-powered predictions  
✅ Smart anomaly detection  
✅ Interactive dashboards  
✅ Advanced analytics  
✅ Downloadable reports  
✅ Real-time visualization  

---

Use the sidebar to navigate through the platform.
""")