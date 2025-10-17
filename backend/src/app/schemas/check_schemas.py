from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .usuario_schemas import UsuarioResponse
from .horario_schemas import HorarioResponse

class CheckBase(BaseModel):
    model_config = {"from_attributes": True}

class CheckCreate(CheckBase):
    usuario_id: int
    horario_id: int

class CheckUpdate(CheckBase):
    usuario_id: Optional[int] = None
    horario_id: Optional[int] = None

class CheckResponse(CheckBase):
    id: int
    usuario_id: int
    horario_id: int
    data_check: datetime
    usuario: Optional[UsuarioResponse] = None
    horario: Optional[HorarioResponse] = None
