from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)

    # Relações - use string references
    horarios = relationship("Horario", back_populates="usuario")
    checks = relationship("Check", back_populates="usuario")