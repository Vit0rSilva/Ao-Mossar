from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base
import uuid

class Admin(Base):
    __tablename__ = "admins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    # ADICIONE ESTAS LINHAS:
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)