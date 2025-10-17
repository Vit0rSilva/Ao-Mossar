from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time
from database.database import Base

class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_refeicao_id = Column(Integer, ForeignKey("tipos_refeicao.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    horario_refeicao = Column(Time, nullable=False)  # Nova coluna

    tipo_refeicao = relationship("TipoRefeicao", back_populates="horarios")
    usuario = relationship("Usuario", back_populates="horarios")
    cardapios = relationship("Cardapio", back_populates="horario")
    checks = relationship("Check", back_populates="horario")