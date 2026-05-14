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
# BRAND HEADER
# --------------------------------
st.markdown("""
<div class="brand-logo">

<div class="brand-icon">
⚡
</div>

<div class="brand-text">
<h1>PowerNova AI</h1>
<p>Smart Energy Intelligence Platform</p>
</div>

</div>
""", unsafe_allow_html=True)

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

The platform simulates smart meter behavior and applies machine learning algorithms to monitor and analyze electricity usage in real time.

### Main Objectives

- Smart electricity monitoring
- AI-based electricity forecasting
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
- Pandas
- NumPy
- Plotly
- Scikit-learn
- GitHub

---

## 📊 Key Features

✅ Live electricity simulation  
✅ AI-powered predictions  
✅ Real-time electricity monitoring  
✅ Interactive dashboards  
✅ Electricity usage analytics  
✅ Downloadable reports  
✅ Real-time visualization  
✅ Machine learning prediction system  

---

## 🔮 Future Enhancements

- IoT smart meter integration
- Cloud deployment
- Mobile application support
- Advanced deep learning models
- Real-time alert system

---

Use the sidebar to navigate through the platform.
""")

st.markdown("---")

st.caption(
    " 2026 PowerNova AI • Intelligent Energy Monitoring Platform"
)