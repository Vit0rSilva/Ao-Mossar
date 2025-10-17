from pydantic import BaseModel, constr, confloat, conint
from typing import Optional

class AlimentoBase(BaseModel):
    unidade_medida: Optional[confloat(ge=0)] = None
    kcal: Optional[confloat(ge=0)] = None
    proteinas: Optional[confloat(ge=0)] = None
    gordura: Optional[confloat(ge=0)] = None
    acucar: Optional[confloat(ge=0)] = None
    carboidratos: Optional[confloat(ge=0)] = None
    unidade: Optional[conint(ge=0)] = None

    model_config = {"from_attributes": True}


class AlimentoCreate(AlimentoBase):
    nome: constr(min_length=1, max_length=100)


class AlimentoUpdate(AlimentoBase):
    nome: Optional[constr(min_length=1, max_length=100)] = None


class AlimentoResponse(AlimentoBase):
    id: int
    nome: constr(min_length=1, max_length=100)
