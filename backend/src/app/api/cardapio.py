from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.schemas import cardapio_schemas, response_schemas
from database.repositories import cardapio_repositories
from src.app.deps import get_db, get_current_usuario, get_current_admin

router = APIRouter(prefix="/cardapios", tags=["Cardapios"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_cardapios(db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    cardapio = cardapio_repositories.get_cardapios(db)

    cardapio_data = [
        cardapio_schemas.CardapioResponse.model_validate(tr).model_dump()
        for tr in cardapio
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de cardapio.",
        data=cardapio_data
    )


@router.get("/{cardapio_id}", response_model=response_schemas.SuccessResponse)
def cardapio_por_id(cardapio_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_usuario)):
    cardapio = cardapio_repositories.get_cardapio(db, cardapio_id)
    if not cardapio:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Cardapio não encontrado",
                "error_code": "NOT_FOUND_CARDAPIO"
            }
        )

    cardapio_data = cardapio_schemas.CardapioResponse.model_validate(cardapio).model_dump()

    return response_schemas.SuccessResponse(
        message="Cardapio encontrado.",
        data=cardapio_data
    )

@router.get("/usuario/todas/{tipo_refeicao}", response_model=response_schemas.SuccessResponse)
def todos_cardapio_refeicao(
    tipo_refeicao: str,
    db: Session = Depends(get_db),
    current_usuario = Depends(get_current_usuario)
):
    cardapio_obj = cardapio_repositories.get_cardapio_usuario_refeicao(current_usuario.telefone, tipo_refeicao, db)
    
    if not cardapio_obj:
        raise HTTPException(status_code=404, detail="Usuário ou Tipo de Refeição não encontrado")

    cardapio_data = cardapio_schemas.CardapioResponse.model_validate(cardapio_obj).model_dump()

    return response_schemas.SuccessResponse(
        message="Cardapio encontrado.",
        data=cardapio_data
    )

@router.get("/admin/{usuario_numero}/{tipo_refeicao}", response_model=response_schemas.SuccessResponse)
def todos_cardapio_refeicao(
    usuario_numero: str,
    tipo_refeicao: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    
    cardapio_obj = cardapio_repositories.get_cardapio_usuario_refeicao(usuario_numero, tipo_refeicao, db)
    
    if not cardapio_obj:
        raise HTTPException(status_code=404, detail="Usuário ou Tipo de Refeição não encontrado")

    cardapio_data = cardapio_schemas.CardapioResponse.model_validate(cardapio_obj).model_dump()

    return response_schemas.SuccessResponse(
        message="Cardapio encontrado.",
        data=cardapio_data
    )

@router.get("/usuarios/todos", response_model=response_schemas.SuccessResponse)
def todos_cardapio_usuario(
    usuario_numero: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    
    cardapios_list = cardapio_repositories.get_cardapio_usuario(current_user.telefone, db)
    
    if not cardapios_list:
        raise HTTPException(
            status_code=404, 
            detail="Usuário não encontrado ou não possui cardápios"
        )

    cardapios_data = [
        cardapio_schemas.CardapioResponse.model_validate(cardapio).model_dump()
        for cardapio in cardapios_list
    ]

    return response_schemas.SuccessResponse(
        message=f"Encontrados {len(cardapios_data)} cardápio(s) para o usuário {usuario_numero}",
        data=cardapios_data
    )

@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_cardapio(
    cardapio: cardapio_schemas.CardapioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    if not cardapio:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_cardapio = cardapio_repositories.create_cardapio(db, cardapio)

    return response_schemas.SuccessResponse(
        message="Cardapio criado com sucesso.",
        data=cardapio_schemas.CardapioResponse.model_validate(novo_cardapio)
    )


@router.put("/{cardapio_id}", response_model=response_schemas.SuccessResponse)
def atualizar_cardapio(
    cardapio_id: int,
    cardapio_data: cardapio_schemas.CardapioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    cardapio_atualizado = cardapio_repositories.update_cardapio(
        db, cardapio_id, cardapio_data
    )

    if not cardapio_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Cardapio não encontrado",
                "error_code": "NOT_FOUND_CARDAPIO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Cardapio atualizado com sucesso.",
        data=cardapio_schemas.CardapioResponse.model_validate(cardapio_atualizado)
    )


@router.delete("/{cardapio_id}", response_model=response_schemas.SuccessResponse)
def deletar_cardapio(
    cardapio_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_usuario)
):
    cardapio = cardapio_repositories.get_cardapio(db, cardapio_id)
    if not cardapio:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Cardapio não encontrado",
                "error_code": "NOT_FOUND_CARDAPIO"
            }
        )

    db.delete(cardapio)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Cardapio deletado com sucesso.",
        data=False
    )
