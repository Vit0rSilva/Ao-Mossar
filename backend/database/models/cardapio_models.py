from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database.database import Base

class Cardapio(Base):
    __tablename__ = "cardapios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horario_id = Column(Integer, ForeignKey("horarios.id"))
    principal = Column(Boolean, default=False)

    horario = relationship("Horario", back_populates="cardapios")
    cardapio_alimentos = relationship("CardapioAlimento", back_populates="cardapio", cascade="all, delete-orphan")