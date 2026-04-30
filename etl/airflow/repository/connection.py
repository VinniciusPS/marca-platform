# airflow/repository/connection.py

from sqlalchemy import create_engine
import os

def get_engine():
    return create_engine(os.environ["DATABASE_URL"])