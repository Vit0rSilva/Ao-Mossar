from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.schemas import tipo_refeicao_schemas, response_schemas
from database.repositories import tipoRefeicao_repositories
from src.app.deps import get_db

router = APIRouter(prefix="/tipo_refeicoes", tags=["Tipo Refeições"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_tipo_refeicoes(db: Session = Depends(get_db)):
    tipos_refeicoes = tipoRefeicao_repositories.get_tipo_refeicoes(db)

    tipos_refeicoes_data = [
        tipo_refeicao_schemas.TipoRefeicaoResponse.model_validate(tr).model_dump()
        for tr in tipos_refeicoes
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de refeição.",
        data=tipos_refeicoes_data
    )


@router.get("/{tipo_refeicao_id}", response_model=response_schemas.SuccessResponse)
def tipo_refeicao_por_id(tipo_refeicao_id: int, db: Session = Depends(get_db)):
    tipo_refeicao = tipoRefeicao_repositories.get_tipo_refeicao(db, tipo_refeicao_id)
    if not tipo_refeicao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Tipo de refeição não encontrado",
                "error_code": "NOT_FOUND_TIPO_REFEICAO"
            }
        )

    tipo_refeicao_data = tipo_refeicao_schemas.TipoRefeicaoResponse.model_validate(tipo_refeicao).model_dump()

    return response_schemas.SuccessResponse(
        message="Tipo de refeição encontrado.",
        data=tipo_refeicao_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_tipo_refeicao(
    tipo_refeicao: tipo_refeicao_schemas.TipoRefeicaoCreate,
    db: Session = Depends(get_db)
):
    if not tipo_refeicao:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_tipo_refeicao = tipoRefeicao_repositories.create_tipo_refeicao(db, tipo_refeicao)

    return response_schemas.SuccessResponse(
        message="Tipo de refeição criado com sucesso.",
        data=tipo_refeicao_schemas.TipoRefeicaoResponse.model_validate(novo_tipo_refeicao)
    )


@router.put("/{tipo_refeicao_id}", response_model=response_schemas.SuccessResponse)
def atualizar_tipo_refeicao(
    tipo_refeicao_id: int,
    tipo_refeicao_data: tipo_refeicao_schemas.TipoRefeicaoUpdate,
    db: Session = Depends(get_db)
):
    tipo_refeicao_atualizado = tipoRefeicao_repositories.update_tipo_refeicao(
        db, tipo_refeicao_id, tipo_refeicao_data
    )

    if not tipo_refeicao_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Tipo de refeição não encontrado",
                "error_code": "NOT_FOUND_TIPO_REFEICAO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Tipo de refeição atualizado com sucesso.",
        data=tipo_refeicao_schemas.TipoRefeicaoResponse.model_validate(tipo_refeicao_atualizado)
    )


@router.delete("/{tipo_refeicao_id}", response_model=response_schemas.SuccessResponse)
def deletar_tipo_refeicao(
    tipo_refeicao_id: int,
    db: Session = Depends(get_db)
):
    tipo_refeicao = tipoRefeicao_repositories.get_tipo_refeicao(db, tipo_refeicao_id)
    if not tipo_refeicao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Tipo de refeição não encontrado",
                "error_code": "NOT_FOUND_TIPO_REFEICAO"
            }
        )

    db.delete(tipo_refeicao)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Tipo de refeição deletado com sucesso.",
        data=False
    )
