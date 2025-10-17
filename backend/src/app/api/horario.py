from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.schemas import horario_schemas, response_schemas
from database.repositories import horario_repositories
from src.app.deps import get_db

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_horarios(db: Session = Depends(get_db)):
    horario = horario_repositories.get_horarios(db)

    horario_data = [
        horario_schemas.HorarioResponse.model_validate(tr).model_dump()
        for tr in horario
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de horario.",
        data=horario_data
    )


@router.get("/{horario_id}", response_model=response_schemas.SuccessResponse)
def horario_por_id(horario_id: int, db: Session = Depends(get_db)):
    horario = horario_repositories.get_horario(db, horario_id)
    if not horario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
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
    db: Session = Depends(get_db)
):
    if not horario:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_horario = horario_repositories.create_horario(db, horario)

    return response_schemas.SuccessResponse(
        message="Horario criado com sucesso.",
        data=horario_schemas.HorarioResponse.model_validate(novo_horario)
    )


@router.put("/{horario_id}", response_model=response_schemas.SuccessResponse)
def atualizar_horario(
    horario_id: int,
    horario_data: horario_schemas.HorarioUpdate,
    db: Session = Depends(get_db)
):
    horario_atualizado = horario_repositories.update_horario(
        db, horario_id, horario_data
    )

    if not horario_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Horario atualizado com sucesso.",
        data=horario_schemas.HorarioResponse.model_validate(horario_atualizado)
    )


@router.delete("/{horario_id}", response_model=response_schemas.SuccessResponse)
def deletar_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):
    horario = horario_repositories.get_horario(db, horario_id)
    if not horario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Horario não encontrado",
                "error_code": "NOT_FOUND_HORARIO"
            }
        )

    db.delete(horario)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Horario deletado com sucesso.",
        data=False
    )
