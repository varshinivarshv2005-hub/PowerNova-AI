import joblib
import pandas as pd
from datetime import datetime

# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------
model = joblib.load("models/forecast_model.pkl")
anomaly_model = joblib.load(
    "models/anomaly_model.pkl"
)

# --------------------------------
# PREDICT FUTURE USAGE
# --------------------------------
def predict_usage(voltage, current):

    # Current hour
    hour = datetime.now().hour

    # Create input dataframe
    input_data = pd.DataFrame({
        "hour": [hour],
        "voltage": [voltage],
        "current": [current]
    })

    # Predict
    prediction = model.predict(input_data)

    return round(prediction[0], 2)
# --------------------------------
# DETECT ANOMALY
# --------------------------------
def detect_anomaly(usage, voltage, current):

    input_data = pd.DataFrame({
        "usage_kwh": [usage],
        "voltage": [voltage],
        "current": [current]
    })

    prediction = anomaly_model.predict(input_data)

    # -1 = anomaly
    if prediction[0] == -1:
        return "⚠ Anomaly Detected"

    else:
        return "✅ Normal"