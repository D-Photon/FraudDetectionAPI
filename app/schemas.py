from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Age: int = Field(ge=0)
    Payment_Type: str = Field(min_length=1)
    AmountWithdraw: float = Field(ge=0, allow_inf_nan=False)
    Old_Balance_Origin: float = Field(ge=0, allow_inf_nan=False)
    New_Balance_Origin: float = Field(ge=0, allow_inf_nan=False)
    Oldbalance_Destination: float = Field(ge=0, allow_inf_nan=False)
    Newbalance_Destination: float = Field(ge=0, allow_inf_nan=False)
    Day: int = Field(ge=1, le=31)
    Day_of_week: int = Field(ge=0, le=6)
    Month: int = Field(ge=1, le=12)


class PredictionData(BaseModel):
    Age: int
    Payment_Type: str
    AmountWithdraw: float
    Old_Balance_Origin: float
    New_Balance_Origin: float
    Oldbalance_Destination: float
    Newbalance_Destination: float
    Day: int
    Day_of_week: int
    Month: int
    Predicted_class: Literal["Fraud", "Legitimate"]
    Fraud_probability: float | None = Field(default=None, ge=0, le=1)
    Date: datetime




