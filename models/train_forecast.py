import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression

# --------------------------------
# LOAD DATASET
# --------------------------------
df = pd.read_csv("data/electricity_data.csv")

# --------------------------------
# FEATURE ENGINEERING
# --------------------------------
df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

# --------------------------------
# FEATURES AND TARGET
# --------------------------------
X = df[["hour", "voltage", "current"]]

y = df["usage_kwh"]

# --------------------------------
# TRAIN MODEL
# --------------------------------
model = LinearRegression()

model.fit(X, y)

# --------------------------------
# SAVE MODEL
# --------------------------------
joblib.dump(
    model,
    "models/forecast_model.pkl"
)

print("Forecast model trained successfully!")