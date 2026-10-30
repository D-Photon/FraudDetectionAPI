# Fraud Detection API : Executive Summary

A machine learning REST API built with FastAPI and LightGBM to classify financial transactions as potentially fraudulent or legitimate. The API accepts transaction details in JSON format, performs the feature engineering required by the trained model, generates a prediction and fraud probability, and stores the prediction record in a connected database.

## Features

- Fraud classification using a trained LightGBM model.
- Transaction input validation using Pydantic schemas.
- Automatic feature engineering before prediction.
- Fraud probability estimation.
- Prediction history storage using SQLAlchemy and PostgreSQL.
- Neon PostgreSQL database integration.
- Interactive API documentation through Swagger UI.
- Docker support for containerized deployment.

## Technology Stack Used

- Python — application and model integration.
- FastAPI — REST API framework.
- LightGBM — machine learning classification algorithm.
- Pandas and NumPy — data processing and feature engineering.
- Scikit-learn — model preprocessing pipeline.
- Pydantic — request and response validation.
- SQLAlchemy — database interaction.
- PostgreSQL (Neon) — prediction history storage.
- Docker — application containerization.

## Project Structure

```text
fraud_detection_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── artifact/
│   └── Fraudmodel_lgbm.pkl
├── .env
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API availability. |
| POST | `/predict` | Predicts the fraud risk of a transaction. |
| GET | `/docs` | Opens the interactive Swagger UI documentation. |

## Making a Prediction

The prediction endpoint accepts transaction details through `POST /predict` as a JSON request.

### Example request

```json
{
  "Age": 35,
  "Payment_Type": "TRANSFER",
  "AmountWithdraw": 2500.0,
  "Old_Balance_Origin": 5000.0,
  "New_Balance_Origin": 2500.0,
  "Oldbalance_Destination": 1000.0,
  "Newbalance_Destination": 3500.0,
  "Day": 12,
  "Day_of_week": 2,
  "Month": 6
}
```

### Prediction workflow

1. The API validates the submitted transaction data.
2. The payment type is mapped to its numerical representation.
3. The API derives the engineered features required by the trained model.
4. The saved LightGBM pipeline generates a predicted class and, where supported, a fraud probability.
5. The API returns the transaction details and prediction result.
6. The prediction record is stored in the connected database.

### Example response

```json
{
  "Age": 35,
  "Payment_Type": "TRANSFER",
  "AmountWithdraw": 2500.0,
  "Old_Balance_Origin": 5000.0,
  "New_Balance_Origin": 2500.0,
  "Oldbalance_Destination": 1000.0,
  "Newbalance_Destination": 3500.0,
  "Day": 12,
  "Day_of_week": 2,
  "Month": 6,
  "Predicted_class": "Legitimate",
  "Fraud_probability": 0.001,
  "Date": "2026-10-29T03:07:25.877Z"
}
```

*The response values above are illustrative; the actual class, probability, and timestamp depend on the submitted transaction and model output.*

## Database and Prediction History

The application uses SQLAlchemy to interact with a database and stores prediction records in the `prediction_records` table.

Each record includes the submitted transaction fields and the model's prediction output, including the predicted class, fraud probability, and prediction timestamp.

The application creates the database table during startup if it does not already exist.

### Neon PostgreSQL configuration

The database connection string is supplied through the `DATABASE_URL` environment variable. For local development, configure it in a `.env` file in the project root:

```env
DATABASE_URL=YOUR_NEON_DATABASE_CONNECTION_STRING
```

Replace the placeholder with your actual Neon connection string. Never commit database credentials or the `.env` file to source control.

The application uses SQLAlchemy and the configured PostgreSQL driver to connect to Neon.

> A predicted fraud classification is not a confirmed fraud outcome. Confirmed transaction outcomes should be recorded separately if they will be used for future model evaluation or retraining.

## Application Components

### `main.py`

Defines the FastAPI application, loads the trained model, validates transaction requests, performs feature engineering, generates predictions, and coordinates prediction storage.

### `schemas.py`

Defines the Pydantic request and response schemas used to validate incoming transaction data and structure prediction responses.

### `models.py`

Defines the SQLAlchemy database model for the prediction records table.

### `database.py`

Manages the database engine, table creation, and persistence of prediction records.

### `Fraudmodel_lgbm.pkl`

Contains the serialized, trained LightGBM pipeline used for inference. The preprocessing steps and feature definitions must remain consistent with those used during model training.


