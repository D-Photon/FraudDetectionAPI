from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.database import create_database_table, save_prediction
from app.schemas import PredictionData, TransactionData


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifact" / "Fraudmodel_lgbm.pkl"

if not MODEL_PATH.is_file():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_database_table()
    yield


app = FastAPI(title="Fraud Detection API", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Fraud Detection API is running"}


@app.post("/predict", response_model=PredictionData)
def predict_fraud(data: TransactionData):
    # Keep feature names consistent with the training data.

    # transform the payment type
    payment_map = {"PAYMENT":0, "TRANSFER":1, "CASH_OUT":2, "DEBIT":3, "CASH_IN":4}
    payment_type = data.Payment_Type.strip().upper()

    if payment_type not in payment_map:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported payment type {payment_type}"
        )

    encoded_payment = payment_map[payment_type]
    
    features = pd.DataFrame([{
        "Age": data.Age,
        "PaymentType": encoded_payment,
        "AmountWithdraw": data.AmountWithdraw,
        "OldBalance": data.Old_Balance_Origin,
        "NewBalance": data.New_Balance_Origin,
        "OldbalanceDestination": data.Oldbalance_Destination,
        "NewbalanceDestination": data.Newbalance_Destination,
        "Day": data.Day,
        "Dayofweek": data.Day_of_week,
        "Month": data.Month,
    }])
    features["DestinationBalanceChange"] = (
        features["NewbalanceDestination"] - features["OldbalanceDestination"]
    )
    features["LogAmount"] = np.log1p(features["AmountWithdraw"])
    features["ExpectedNewBalance_Sender"] = (
        features["OldBalance"] - features["AmountWithdraw"]
    )
    features["SenderBalanceError"] = (
        features["NewBalance"] - features["ExpectedNewBalance_Sender"]
    )

    try:
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features) if hasattr(model, "predict_proba") else None
        fraud_probability = float(probabilities[0][1]) if probabilities is not None else None
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not score this input: {exc}") from exc

    prediction_time = datetime.now(timezone.utc)
    predicted_class = "Fraud" if prediction == 1 else "Legitimate"

    result = {
        "Age": data.Age,
        "Payment_Type": data.Payment_Type,
        "AmountWithdraw": data.AmountWithdraw,
        "Old_Balance_Origin": data.Old_Balance_Origin,
        "New_Balance_Origin": data.New_Balance_Origin,
        "Oldbalance_Destination": data.Oldbalance_Destination,
        "Newbalance_Destination": data.Newbalance_Destination,
        "Day": data.Day,
        "Day_of_week": data.Day_of_week,
        "Month": data.Month,
        "Predicted_class": predicted_class,
        "Fraud_probability": fraud_probability,
        "Date": prediction_time,
    }

    try:
        save_prediction({
            **{key: value for key, value in result.items() if key not in {"Date"}},
            "DestinationBalanceChange": float(features["DestinationBalanceChange"].iloc[0]),
        })
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction succeeded but could not be saved") from exc

    return result



