from pydantic import BaseModel
from typing import Optional
from .alimento_schemas import AlimentoResponse

class CardapioAlimentoBase(BaseModel):
    model_config = {"from_attributes": True}

class CardapioAlimentoCreate(CardapioAlimentoBase):
    cardapio_id: int
    alimento_id: int

class CardapioAlimentoUpdate(CardapioAlimentoBase):
    cardapio_id: Optional[int] = None
    alimento_id: Optional[int] = None

class CardapioAlimentoResponse(CardapioAlimentoBase):
    id: int
    cardapio_id: int
    alimento_id: int
    alimento: Optional[AlimentoResponse] = None
