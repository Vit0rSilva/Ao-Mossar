from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from .tipo_refeicao_schemas import TipoRefeicaoResponse
from .usuario_schemas import UsuarioResponse

class HorarioBase(BaseModel):
    model_config = {"from_attributes": True}

class HorarioCreate(HorarioBase):
    tipo_refeicao_id: int
    usuario_id: int
    horario_refeicao: time

class HorarioUpdate(HorarioBase):
    tipo_refeicao_id: Optional[int] = None
    usuario_id: Optional[int] = None
    horario_refeicao: Optional[time] = None

class HorarioResponse(HorarioBase):
    id: int
    tipo_refeicao_id: int
    usuario_id: int
    horario_refeicao: time
    tipo_refeicao: Optional[TipoRefeicaoResponse] = None
    usuario: Optional[UsuarioResponse] = None
    """usuario: Optional[UsuarioResponse] = None"""