from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database.database import Base

class TipoRefeicao(Base):
    __tablename__ = "tipos_refeicao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)

    horarios = relationship("Horario", back_populates="tipo_refeicao")