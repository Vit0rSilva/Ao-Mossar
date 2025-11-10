from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.schemas import check_schemas, response_schemas
from database.repositories import check_repositories
from database.models.usuario_models import Usuario
from src.app.service.pertencimento_service import PertencimentoService
from src.app.deps import get_db, get_current_admin, get_current_usuario, get_pertencimento_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/check", tags=["Check"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_checks(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    check = check_repositories.get_checks(db)

    check_data = [
        check_schemas.CheckResponse.model_validate(tr).model_dump()
        for tr in check
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de check.",
        data=check_data
    )

@router.get("/usuario/todos", response_model=response_schemas.SuccessResponse)
def listar_checks(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    check = check_repositories.get_checks_usuario(db, current_user.id)

    check_data = [
        check_schemas.CheckResponse.model_validate(tr).model_dump()
        for tr in check
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de check.",
        data=check_data
    )

@router.get("/{check_id}", response_model=response_schemas.SuccessResponse)
def check_por_id(check_id: int, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=50, minutes=30))             
    ):
    tem_permissao = pertencimento_service.verificar_pertecimento_check(check_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O check não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_CHECK"
            }
        )
    check = check_repositories.get_check(db, check_id)
    if not check:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Check não encontrado",
                "error_code": "NOT_FOUND_CHECK"
            }
        )

    check_data = check_schemas.CheckResponse.model_validate(check).model_dump()

    return response_schemas.SuccessResponse(
        message="Check encontrado.",
        data=check_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_check(
    check: check_schemas.CheckCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    #limiter: RateLimiter = Depends(RateLimiter(times=50, minutes=30))   
):
    if not check:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_check = check_repositories.create_check(db, check, current_user.id)

    return response_schemas.SuccessResponse(
        message="Check criado com sucesso.",
        data=check_schemas.CheckResponse.model_validate(novo_check)
    )


@router.put("/{check_id}", response_model=response_schemas.SuccessResponse)
def atualizar_check(
    check_id: int,
    check_data: check_schemas.CheckUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=40, minutes=30))            
):
    tem_permissao = pertencimento_service.verificar_pertecimento_check(check_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O check não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_CHECK"
            }
        )
    check_atualizado = check_repositories.update_check(
        db, check_id, check_data
    )

    if not check_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Check não encontrado",
                "error_code": "NOT_FOUND_CHECK"
            }
        )

    return response_schemas.SuccessResponse(
        message="Check atualizado com sucesso.",
        data=check_schemas.CheckResponse.model_validate(check_atualizado)
    )


@router.delete("/{check_id}", response_model=response_schemas.SuccessResponse)
def deletar_check(
    check_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=30, minutes=30))       
):
    tem_permissao = pertencimento_service.verificar_pertecimento_check(check_id, current_user.id)
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O check não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_CHECK"
            }
        )
    check = check_repositories.get_check(db, check_id)
    if not check:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Check não encontrado",
                "error_code": "NOT_FOUND_CHECK"
            }
        )

    db.delete(check)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Check deletado com sucesso.",
        data=False
    )
