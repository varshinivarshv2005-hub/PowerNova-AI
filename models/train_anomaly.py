import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest

# --------------------------------
# LOAD DATASET
# --------------------------------
df = pd.read_csv("data/electricity_data.csv")

# --------------------------------
# FEATURES
# --------------------------------
X = df[["usage_kwh", "voltage", "current"]]

# --------------------------------
# TRAIN MODEL
# --------------------------------
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

# --------------------------------
# SAVE MODEL
# --------------------------------
joblib.dump(
    model,
    "models/anomaly_model.pkl"
)

print("Anomaly detection model trained successfully!")