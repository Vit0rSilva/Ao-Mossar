from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database.database import Base 

class CardapioAlimento(Base):
    __tablename__ = "cardapio_alimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cardapio_id = Column(Integer, ForeignKey("cardapios.id"))
    alimento_id = Column(Integer, ForeignKey("alimentos.id"))

    cardapio = relationship("Cardapio", back_populates="cardapio_alimentos")
    alimento = relationship("Alimento", back_populates="cardapio_alimentos")