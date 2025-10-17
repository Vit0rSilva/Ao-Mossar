from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database.database import Base

class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    unidade_medida = Column(Numeric(10, 1), nullable=True)
    kcal = Column(Numeric(10, 1), nullable=True)
    proteinas = Column(Numeric(10, 1), nullable=True)
    gordura = Column(Numeric(10, 1), nullable=True)
    acucar = Column(Numeric(10, 1), nullable=True)
    carboidratos  = Column(Numeric(10, 1), nullable=True)

    unidade = Column(Integer, nullable=True)


    cardapio_alimentos = relationship("CardapioAlimento", back_populates="alimento")