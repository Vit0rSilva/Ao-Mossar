# app/repositories/admin_repositories.py
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import secrets

from database.models.admin_models import Admin
from src.app.schemas.admin_schemas import AdminCreate

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_admins(self):
        return self.db.query(Admin).all()


    def get_admin(self, admin_id: int):
        return self.db.query(Admin).filter(
            Admin.id == admin_id
        ).first()

    def get_admin_numero(self, numero: str):
        return self.db.query(Admin).filter(
            Admin.telefone == numero
        ).first()

    def get_by_email(self, email: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.email == email).first()

    def get_by_id(self, id: str | UUID) -> Optional[Admin]:
        try:
            id_str = str(UUID(str(id)))
        except (ValueError, TypeError):
            return None
        return self.db.query(Admin).filter(Admin.id == id_str).first()

    def create(self, admin_create: AdminCreate, hashed_password: str) -> Admin:
        admin = Admin(
            nome=admin_create.nome,
            email=admin_create.email,
            telefone=admin_create.telefone,
            senha=hashed_password,
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def update(self, admin: Admin) -> Admin:
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin