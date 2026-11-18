import os
import joblib
import pandas as pd

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from huggingface_hub import hf_hub_download


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

MODEL_REPO = "fawad-archAI/building-energy-forecasting-rf-advanced"
MODEL_FILENAME = "random_forest_advanced.pkl"

model_path = hf_hub_download(
    repo_id=MODEL_REPO,
    filename=MODEL_FILENAME
)

model = joblib.load(model_path)

print("Random Forest model loaded successfully!")


# ==========================================
# 2. CREATE API
# ==========================================

app = FastAPI(
    title="Building Energy Forecasting API",
    description="Predicts the next hourly building energy reading.",
    version="1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. DEFINE USER INPUT
# ==========================================

class PredictionInput(BaseModel):

    historical_readings: list[float] = Field(
        ...,
        min_length=48,
        max_length=48
    )

    next_timestamp: datetime


# ==========================================
# 4. FEATURE ENGINEERING
# ==========================================

def create_features(readings, timestamp):

    features = {

        "lag_1": readings[-1],
        "lag_2": readings[-2],
        "lag_3": readings[-3],

        "lag_24": readings[-24],
        "lag_48": readings[-48],

        "hour": timestamp.hour,
        "day_of_week": timestamp.weekday(),

        "is_weekend": int(timestamp.weekday() >= 5),

        "rolling_mean_3": sum(readings[-3:]) / 3,

        "rolling_mean_24": sum(readings[-24:]) / 24
    }

    return pd.DataFrame([features])


# ==========================================
# 5. PREDICTION ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Building Energy Forecasting API is running!"
    }


@app.post("/predict")
def predict(data: PredictionInput):

    try:

        readings = data.historical_readings
        timestamp = data.next_timestamp

        if not all(pd.notna(value) for value in readings):
            raise ValueError("Readings must contain valid numbers.")

        if timestamp.minute != 0 or timestamp.second != 0:
            raise ValueError(
                "Prediction timestamp must be on the hour."
            )

        features = create_features(readings, timestamp)

        prediction = model.predict(features)[0]

        return {
            "predicted_reading": round(float(prediction), 3),
            "prediction_timestamp": timestamp.isoformat(),
            "model": "Advanced Random Forest (300 trees)"
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )