# app/repositories/usuario_repositories.py
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import secrets

from database.models.usuario_models import Usuario
from src.app.schemas.usuario_schemas import UsuarioCreate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_usuarios(self):
        return self.db.query(Usuario).all()


    def get_usuario(self, usuario_id: int):
        return self.db.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

    def get_usuario_numero(self, numero: str):
        return self.db.query(Usuario).filter(
            Usuario.telefone == numero
        ).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_id(self, id: str | UUID) -> Optional[Usuario]:
        try:
            id_str = str(UUID(str(id)))
        except (ValueError, TypeError):
            return None
        return self.db.query(Usuario).filter(Usuario.id == id_str).first()

    def create(self, usuario_create: UsuarioCreate, hashed_password: str) -> Usuario:
        usuario = Usuario(
            nome=usuario_create.nome,
            email=usuario_create.email,
            telefone=usuario_create.telefone,
            senha=hashed_password,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario