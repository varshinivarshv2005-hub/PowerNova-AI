import streamlit as st

from utils.database import fetch_data
from utils.analytics import predict_usage

st.title("🔮 AI Predictions")

df = fetch_data()

latest = df.iloc[-1]

prediction = predict_usage(
    latest["voltage"],
    latest["current"]
)

st.metric(
    "Predicted Future Usage (kWh)",
    prediction
)

st.info(
    "Prediction generated using Linear Regression model."
)