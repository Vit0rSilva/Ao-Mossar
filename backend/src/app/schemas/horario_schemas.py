from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time
from .tipo_refeicao_schemas import TipoRefeicaoResponse
from .usuario_schemas import UsuarioResponse
from .cardapio_alimento_schemas import CardapioAlimentoResponse
from .cardapio_schemas import CardapioResponse

class HorarioBase(BaseModel):
    model_config = {"from_attributes": True}

class HorarioCreate(HorarioBase):
    tipo_refeicao_id: int
    usuario_id: str
    horario_refeicao: time

class HorarioUpdate(HorarioBase):
    tipo_refeicao_id: Optional[int] = None
    usuario_id: Optional[str] = None
    horario_refeicao: Optional[time] = None

class HorarioResponse(HorarioBase):
    id: int
    tipo_refeicao_id: int
    usuario_id: str
    horario_refeicao: time
    tipo_refeicao: Optional[TipoRefeicaoResponse] = None
    usuario: Optional[UsuarioResponse] = None
    cardapios: List["CardapioResponse"] = []