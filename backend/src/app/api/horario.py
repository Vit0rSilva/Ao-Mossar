from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from src.app.schemas import horario_schemas, response_schemas
from database.repositories import horario_repositories
from src.app.service.pertencimento_service import PertencimentoService
from src.app.deps import get_db, get_pertencimento_service, get_current_usuario, get_current_admin

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_horarios(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    horario = horario_repositories.get_horarios(db)

    horario_data = [
        horario_schemas.HorarioResponse.model_validate(tr).model_dump()
        for tr in horario
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de horario.",
        data=horario_data
    )

# Em /src/app/api/cardapio.py

# 1. Você vai precisar importar o schema de Horario
from src.app.schemas import horario_schemas # <-- ADICIONE ESTE IMPORT

@router.get("/usuarios/todos", response_model=response_schemas.SuccessResponse)
def todos_cardapio_usuario(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    
    # 2. Renomeie a variável para clareza (ela recebe Horarios)
    horarios_list = horario_repositories.get_cardapio_usuario(current_user.telefone, db)



    horarios_data = [
        horario_schemas.HorarioResponse.model_validate(horario).model_dump()
        for horario in horarios_list
    ]

    return response_schemas.SuccessResponse(

        message=f"Encontrados {len(horarios_data)} horário(s)", 
        data=horarios_data
    )


@router.get("/{horario_id}", response_model=response_schemas.SuccessResponse)
def horario_por_id(horario_id: int, db: Session = Depends(get_db), 
    current_user = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))                     
    ):
    tem_permissao = pertencimento_service.verificar_pertecimento_horario(horario_id, current_user.id)
    horario = horario_repositories.get_horario(db, horario_id)
    if not horario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
            }
        )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O cardápio não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    horario_data = horario_schemas.HorarioResponse.model_validate(horario).model_dump()

    return response_schemas.SuccessResponse(
        message="Horario encontrado.",
        data=horario_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_horario(
    horario: horario_schemas.HorarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    # ... (validações iniciais) ...

    # Tenta criar
    novo_horario = horario_repositories.create_horario(db, horario, current_user.id)

    # 👇 VERIFICA SE FALHOU
    if not novo_horario:
         raise HTTPException(
            status_code=403, # Forbidden (ou 400 Bad Request)
            detail="Você não tem permissão para criar um horário para outro usuário."
        )

    # Se chegou aqui, deu certo
    return response_schemas.SuccessResponse(
        message="Horario criado com sucesso.",
        data=horario_schemas.HorarioResponse.model_validate(novo_horario)
    )


@router.put("/{horario_id}", response_model=response_schemas.SuccessResponse)
def atualizar_horario(
    horario_id: int,
    horario_data: horario_schemas.HorarioUpdate,
    current_user = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service)     ,
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))                  
):
    tem_permissao = pertencimento_service.verificar_pertecimento_horario(horario_id, current_user.id)
    horario_atualizado = horario_repositories.update_horario(
        pertencimento_service.db, horario_id, horario_data
    )

    if not horario_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
            }
        )

    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O cardápio não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Horario atualizado com sucesso.",
        data=horario_schemas.HorarioResponse.model_validate(horario_atualizado)
    )


@router.delete("/{horario_id}", response_model=response_schemas.SuccessResponse)
def deletar_horario(
    horario_id: int,
    current_user = Depends(get_current_usuario),
    pertencimento_service: PertencimentoService = Depends(get_pertencimento_service),
    #limiter: RateLimiter = Depends(RateLimiter(times=100, minutes=30))                      
):
    tem_permissao = pertencimento_service.verificar_pertecimento_horario(horario_id, current_user.id)
    horario = horario_repositories.get_horario(pertencimento_service.db, horario_id)
    if not horario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
            }
        )
    
    if not tem_permissao:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "O cardápio não foi encontrado ou não pertence a este usuário.",
                "error_code": "NOT_FOUND_ALIMENTO"
            }
        )

    pertencimento_service.db.delete(horario)
    pertencimento_service.db.commit()

    return response_schemas.SuccessResponse(
        message="Horario deletado com sucesso.",
        data=False
    )
