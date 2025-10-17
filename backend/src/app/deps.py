from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import SessionLocal
import jwt
import os
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")
oauth2_usuario_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

SECRET_KEY = os.getenv("SECRET_KEY", "troque_por_alguma_secret_na_producao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

