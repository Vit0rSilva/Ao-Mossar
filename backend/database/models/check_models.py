from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database.database import Base

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String(36), ForeignKey("usuarios.id"))
    horario_id = Column(Integer, ForeignKey("horarios.id"))
    data_check = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="checks")
    horario = relationship("Horario", back_populates="checks")