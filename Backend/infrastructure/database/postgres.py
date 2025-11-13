import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from infrastructure.database.sql_models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db(max_attempts=10, delay=3):
    engine = create_engine(DATABASE_URL)
    
    for attempt in range(max_attempts):
        try:
            with engine.connect():
                print("Database is ready! Continuing application startup.")
                return
        except OperationalError as e:
            print(f"Database not ready yet (Attempt {attempt+1}/{max_attempts}). Retrying in {delay}s...")
            time.sleep(delay)
    
    raise Exception("Failed to connect to the database after multiple attempts.")