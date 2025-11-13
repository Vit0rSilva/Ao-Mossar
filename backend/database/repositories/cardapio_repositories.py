from sqlalchemy.orm import Session
from database.models.cardapio_models import Cardapio
from database.repositories.horario_repositories import get_horarios_refeicao, get_horarios_usuario
from src.app.schemas.cardapio_schemas import CardapioCreate, CardapioUpdate
from src.app.service.pertencimento_service import PertencimentoService



def get_cardapios(db: Session):
    return db.query(Cardapio).all()


def get_cardapio(db: Session, cardapio_id: int):
    return db.query(Cardapio).filter(
        Cardapio.id == cardapio_id
    ).first()

def get_cardapio_usuario_refeicao(usuario_numero:str, tipo_refeicao:str, db):

    horario = get_horarios_refeicao(usuario_numero, tipo_refeicao, db)

    if not horario:
        return None

    return db.query(Cardapio).filter(
        Cardapio.horario_id == horario.id
    ).first()

def get_cardapio_usuario(usuario_numero: str, db: Session):
    """Busca TODOS os cardápios de TODOS os horários de um usuário"""
    horarios = get_horarios_usuario(usuario_numero, db)

    if not horarios:
        return None

    horario_ids = [horario.id for horario in horarios]
    
    return db.query(Cardapio).filter(
        Cardapio.horario_id.in_(horario_ids)
    ).all()

def create_cardapio(db: Session, cardapio: CardapioCreate, usuario_id):
    pertencimento_service = PertencimentoService(db=db)

    if not pertencimento_service.verificar_pertecimento_horario(cardapio.horario_id, usuario_id): return False
    
    # Converte o Pydantic em dicionário
    cardapio_data = cardapio.model_dump()

    # Verifica se já existe algum cardápio para o mesmo horário
    cardapio_existente = (
        db.query(Cardapio)
        .filter(Cardapio.horario_id == cardapio.horario_id)
        .first()
    )

    # Se for o primeiro cardápio do horário → define como principal
    if not cardapio_existente:
        cardapio_data["principal"] = True
    else:
        # Se o novo cardápio vier como principal, desativa o anterior
        if cardapio_data.get("principal") is True:
            cardapio_principal = (
                db.query(Cardapio)
                .filter(
                    Cardapio.horario_id == cardapio.horario_id,
                    Cardapio.principal == True
                )
                .first()
            )
            if cardapio_principal:
                cardapio_principal.principal = False
                db.commit()

    # Cria o novo cardápio
    novo_cardapio = Cardapio(**cardapio_data)
    db.add(novo_cardapio)
    db.commit()
    db.refresh(novo_cardapio)

    return novo_cardapio



def update_cardapio(db: Session, cardapio_id: int, cardapio_data: CardapioUpdate):
    
    update_data = cardapio_data.model_dump(exclude_unset=True)

    cardapio = db.query(Cardapio).filter(Cardapio.id == cardapio_id).first()

    if not cardapio:
        return None

    if update_data.get('principal') is True:
        
        db.query(Cardapio).filter(
            Cardapio.horario_id == cardapio.horario_id, # Do mesmo horário
            Cardapio.id != cardapio_id               # Que NÃO seja este
        ).update(
            {Cardapio.principal: False}, 
            synchronize_session=False  
        )

    for key, value in update_data.items():
        setattr(cardapio, key, value)

    try:
        db.commit()
        db.refresh(cardapio)
    except Exception as e:
        db.rollback() # Desfaz tudo se der erro
        raise e # Retorna o erro
        
    return cardapio