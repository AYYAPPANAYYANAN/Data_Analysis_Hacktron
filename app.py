# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(
    title="Olist Logistics Real-Time Inference API",
    description="Production-grade REST API for predicting late delivery risk at customer checkout.",
    version="1.0.0"
)

# Load model artifacts at startup
MODEL_PATH = "data/processed/model.pkl"
THRESHOLD_PATH = "data/processed/threshold.pkl"
FEATURES_PATH = "data/processed/features.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model binaries not found! Please run 'python main.py' first to train and persist the model.")

model = joblib.load(MODEL_PATH)
optimal_threshold = joblib.load(THRESHOLD_PATH)
model_features = joblib.load(FEATURES_PATH)

class CheckoutRequest(BaseModel):
    approval_lag_hours: float = Field(..., description="Hours elapsed between purchase and payment approval")
    seller_historical_processing_days: float = Field(..., description="Seller's expanding average fulfillment duration")
    seller_historical_late_rate: float = Field(..., description="Seller's expanding historical late delivery rate")
    is_peak_macro_season: int = Field(..., description="Binary flag (0 or 1) indicating peak macro shopping season")
    product_weight_g: float = Field(..., description="Product weight in grams")
    freight_to_price_ratio: float = Field(..., description="Ratio of freight cost to product price")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Olist Logistics Predictive MLOps API",
        "decision_threshold": optimal_threshold
    }

@app.post("/predict")
def predict_late_risk(payload: CheckoutRequest):
    try:
        # Convert incoming payload to DataFrame matching feature ordering
        input_data = pd.DataFrame([payload.dict()])[model_features]
        
        # Inference
        probability = float(model.predict_proba(input_data)[:, 1][0])
        is_late_predicted = int(probability >= optimal_threshold)
        
        risk_tier = "HIGH" if probability >= optimal_threshold else "LOW"
        
        return {
            "predicted_late_risk": is_late_predicted,
            "late_probability": round(probability, 4),
            "decision_threshold": round(optimal_threshold, 4),
            "risk_tier": risk_tier,
            "operational_recommendation": "Route through expedited regional hub or flag SLA warning" if risk_tier == "HIGH" else "Standard fulfillment routing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))