from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.repositories.admin_repositories import AdminRepository
from database.repositories.usuario_repositories import UsuarioRepository
from src.app.service.pertencimento_service import PertencimentoService
import jwt
import os
from uuid import UUID
from typing import Optional
import secrets

oauth2_admin_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")
oauth2_usuario_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

#SECRET_KEY = os.getenv("SECRET_KEY", "91SxMtIc0WMEQGpOhTOI2aq6f5szg8zU4QLCutBJ")
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY não foi definida no .env")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Admininstrador
def get_admin_repo(db: Session = Depends(get_db)) -> AdminRepository:
    return AdminRepository(db)

def get_current_admin(token: str = Depends(oauth2_admin_scheme), repo: AdminRepository = Depends(get_admin_repo)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], leeway=10)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.ImmatureSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ainda não válido (iat)", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise credentials_exception

    sub = payload.get("sub")
    if sub is None:
        raise credentials_exception

    try:
        sub_str = str(UUID(str(sub)))
    except (ValueError, TypeError):
        raise credentials_exception

    user = repo.get_by_id(sub_str)
    if user is None:
        raise credentials_exception

    return user

#Usuario
def get_usuario_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepository(db)

def get_current_usuario(token: str = Depends(oauth2_usuario_scheme), repo: UsuarioRepository = Depends(get_usuario_repo)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], leeway=10)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.ImmatureSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ainda não válido (iat)", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise credentials_exception

    sub = payload.get("sub")
    if sub is None:
        raise credentials_exception

    try:
        sub_str = str(UUID(str(sub)))
    except (ValueError, TypeError):
        raise credentials_exception

    user = repo.get_by_id(sub_str)
    if user is None:
        raise credentials_exception

    return user

def get_pertencimento_service(db: Session = Depends(get_db)) -> PertencimentoService:
    """
    Dependência que cria e retorna uma instância do PertencimentoService.
    """
    return PertencimentoService(db=db)