from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer, nullable=False)
    Payment_Type = Column(String, nullable=False)
    AmountWithdraw = Column(Float, nullable=False)
    Old_Balance_Origin = Column(Float, nullable=False)
    New_Balance_Origin = Column(Float, nullable=False)
    Oldbalance_Destination = Column(Float, nullable=False)
    Newbalance_Destination = Column(Float, nullable=False)
    DestinationBalanceChange = Column(Float, nullable=False)
    Day = Column(Integer, nullable=False)
    Day_of_week = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
    Predicted_class = Column(String, nullable=False)
    Fraud_probability = Column(Float, nullable=True)
    Date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)



    
