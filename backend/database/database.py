from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_CONNECTION_URI_PYTHON = os.getenv("DATABASE_CONNECTION_URI_PYTHON")

engine = create_engine(DATABASE_CONNECTION_URI_PYTHON)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
