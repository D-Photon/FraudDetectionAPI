import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.models import Base, PredictionRecord


PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Neon commonly provides a postgresql:// URL. SQLAlchemy needs an installed
    # DBAPI driver, so explicitly select psycopg 3 for PostgreSQL URLs.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = "postgresql://" + DATABASE_URL.removeprefix("postgres://")
    if DATABASE_URL.startswith("postgresql://"):
        database_url = "postgresql+psycopg://" + DATABASE_URL.removeprefix("postgresql://")
    else:
        database_url = DATABASE_URL
else:
    database_url = URL.create(
        "sqlite", database=str(PROJECT_DIR / "fraud_predictions.db")
    )

is_sqlite = str(database_url).startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_database_table():
    Base.metadata.create_all(bind=engine)


def save_prediction(record_data: dict):
    db = SessionLocal()
    try:
        record = PredictionRecord(**record_data)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
