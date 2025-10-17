from pydantic import BaseModel, constr
from typing import Optional

class TipoRefeicaoBase(BaseModel):
    model_config = {"from_attributes": True}

class TipoRefeicaoCreate(TipoRefeicaoBase):
    nome: constr(min_length=1, max_length=50)

class TipoRefeicaoUpdate(TipoRefeicaoBase):
    nome: Optional[constr(min_length=1, max_length=50)] = None

class TipoRefeicaoResponse(TipoRefeicaoBase):
    id: int
    nome: constr(min_length=1, max_length=50)
