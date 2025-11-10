from pydantic import BaseModel
from typing import Optional, List
#from .horario_schemas import HorarioResponse
from .cardapio_alimento_schemas import CardapioAlimentoResponse

class CardapioBase(BaseModel):
    model_config = {"from_attributes": True}

class CardapioCreate(CardapioBase):
    horario_id: int
    principal: Optional[bool] = None

class CardapioUpdate(CardapioBase):
    horario_id: Optional[int] = None
    principal: Optional[bool] = None

class CardapioResponse(CardapioBase):
    id: int
    horario_id: int
    principal: Optional[bool] = None
    cardapio_alimentos: List[CardapioAlimentoResponse] = []
