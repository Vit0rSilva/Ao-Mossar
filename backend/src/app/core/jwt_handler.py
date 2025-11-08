# app/core/jwt_handler.py
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import os

# ideal: carregar via variáveis de ambiente
#SECRET_KEY = os.getenv("SECRET_KEY", "91SxMtIc0WMEQGpOhTOI2aq6f5szg8zU4QLCutBJ")
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY não foi definida no .env")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h por padrão

def create_access_token(subject: str, extra_claims: dict | None = None, expires_minutes: int | None = None):
    # Ajusta para o fuso horário de Brasília (UTC−3)
    now = datetime.now(timezone.utc) - timedelta(hours=3)
    
    if expires_minutes is None:
        expires_minutes = 1440  # padrão: 24h
    
    expire = now + timedelta(minutes=expires_minutes)

    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "typ": "access"
    }

    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "expires_in": expires_minutes * 60}