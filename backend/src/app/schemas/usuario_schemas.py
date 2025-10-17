from pydantic import BaseModel, constr
from typing import Optional

class UsuarioBase(BaseModel):
    model_config = {"from_attributes": True}

class UsuarioCreate(UsuarioBase):
    nome: constr(min_length=1, max_length=100)
    telefone: constr(min_length=8, max_length=20)

class UsuarioUpdate(UsuarioBase):
    nome: Optional[constr(min_length=1, max_length=100)] = None
    telefone: Optional[constr(min_length=8, max_length=20)] = None

class UsuarioResponse(UsuarioBase):
    id: int
    nome: constr(min_length=1, max_length=100)
    telefone: constr(min_length=8, max_length=20)