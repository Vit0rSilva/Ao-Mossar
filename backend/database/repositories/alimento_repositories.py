from sqlalchemy.orm import Session
from database.models.alimento_models import Alimento
from database.models.cardapio_alimento_models import CardapioAlimento
from src.app.schemas.alimento_schemas import AlimentoCreate, AlimentoUpdate
from src.app.schemas.cardapio_alimento_schemas import CardapioAlimentoCreate
from src.app.service.pertencimento_service import PertencimentoService

def get_alimentos(db: Session):
    return db.query(Alimento).all()


def get_alimento(db: Session, alimento_id: int):
    return db.query(Alimento).filter(
        Alimento.id == alimento_id
    ).first()

def get_cardapio_alimento(db: Session, alimento_id: int):
    return db.query(CardapioAlimento).filter(
        CardapioAlimento.alimento_id == alimento_id
    ).first()



def create_alimento(db: Session, alimento: AlimentoCreate, cardapio_id : int, usuario_id:str):
    pertencimento_service = PertencimentoService(db=db)
    if not pertencimento_service.verificar_pertecimento_cardapio(cardapio_id, usuario_id): return False
    # Cria o alimento
    novo_alimento = Alimento(**alimento.model_dump())
    db.add(novo_alimento)
    db.commit()
    db.refresh(novo_alimento)

    # Cria o relacionamento cardapio_alimento
    cardapio_alimento_data = {
        "cardapio_id": cardapio_id,
        "alimento_id": novo_alimento.id
    }

    novo_cardapio_alimento = CardapioAlimento(**cardapio_alimento_data)
    db.add(novo_cardapio_alimento)
    db.commit()
    db.refresh(novo_cardapio_alimento)

    return novo_cardapio_alimento



def update_alimento(db: Session, alimento_id: int, alimento_data: AlimentoUpdate):
    alimento = db.query(Alimento).filter(
        Alimento.id == alimento_id
    ).first()

    if not alimento:
        return None

    for key, value in alimento_data.model_dump(exclude_unset=True).items():
        setattr(alimento, key, value)

    db.commit()
    db.refresh(alimento)
    return alimento
