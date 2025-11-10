from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from src.app.schemas import alimento_schemas, cardapio_alimento_schemas, response_schemas
from database.repositories import alimento_repositories
from database.models.usuario_models import Usuario
from src.app.service.pertencimento_service import PertencimentoService
from src.app.deps import get_db, get_current_usuario, get_current_admin, get_pertencimento_service

router = APIRouter(prefix="/alimentos", tags=["Alimentos"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_alimentos(db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    alimento = alimento_repositories.get_alimentos(db)

    alimento_data = [
        alimento_schemas.AlimentoResponse.model_validate(tr).model_dump()
        for tr in alimento
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de alimento.",
        data=alimento_data
    )


@router.get("/{alimento_id}", response_model=response_schemas.SuccessResponse)
def alimento_por_id(alimento_id: int, db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_usuario),
        pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
        #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))
    ):
    tem_permissao = pertencimento_service.verificar_pertecimento_alimento(alimento_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O alimento não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )
    alimento = alimento_repositories.get_alimento(db, alimento_id)
    if not alimento:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Alimento não encontrado",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    alimento_data = alimento_schemas.AlimentoResponse.model_validate(alimento).model_dump()

    return response_schemas.SuccessResponse(
        message="Alimento encontrado.",
        data=alimento_data
    )


@router.post("/{cardapio_id}", response_model=response_schemas.SuccessResponse)
def criar_alimento(
    cardapio_id: int,
    alimento: alimento_schemas.AlimentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))
):

    if not alimento:
        raise HTTPException(status_code=400, detail={
            "message":"Dados inválidos",
            "error_code": "DADOS_INVALID"
            })


    novo_alimento = alimento_repositories.create_alimento(db, alimento, cardapio_id, current_user.id)

    return response_schemas.SuccessResponse(
        message="Alimento criado com sucesso.",
        data=cardapio_alimento_schemas.CardapioAlimentoResponse.model_validate(novo_alimento)
    )


@router.put("/{alimento_id}", response_model=response_schemas.SuccessResponse)
def atualizar_alimento(
    alimento_id: int,
    alimento_data: alimento_schemas.AlimentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))
):
    tem_permissao = pertencimento_service.verificar_pertecimento_alimento(alimento_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O alimento não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )
    alimento_atualizado = alimento_repositories.update_alimento(
        db, alimento_id, alimento_data
    )

    if not alimento_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Alimento não encontrado",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Alimento atualizado com sucesso.",
        data=alimento_schemas.AlimentoResponse.model_validate(alimento_atualizado)
    )


@router.delete("/{alimento_id}", response_model=response_schemas.SuccessResponse)
def deletar_alimento(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))
):
    tem_permissao = pertencimento_service.verificar_pertecimento_alimento(alimento_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O alimento não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )
    alimento = alimento_repositories.get_alimento(db, alimento_id)
    if not alimento:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Alimento não encontrado",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    db.delete(alimento)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Alimento deletado com sucesso.",
        data=False
    )
