from sqlalchemy.orm import Session
from database.models.tipo_refeicao_models import TipoRefeicao
from src.app.schemas.tipo_refeicao_schemas import TipoRefeicaoCreate, TipoRefeicaoUpdate

def get_tipo_refeicoes(db: Session):
    return db.query(TipoRefeicao).all()


def get_tipo_refeicao(db: Session, tipo_refeicao_id: int):
    return db.query(TipoRefeicao).filter(
        TipoRefeicao.id == tipo_refeicao_id
    ).first()

def get_tipo_refeicao_nome(db: Session, tipo_refeicao: str):
    return db.query(TipoRefeicao).filter(
        TipoRefeicao.nome == tipo_refeicao
    ).first()

def create_tipo_refeicao(db: Session, tipo_refeicao: TipoRefeicaoCreate):
    novo_tipo_refeicao = TipoRefeicao(**tipo_refeicao.model_dump())
    db.add(novo_tipo_refeicao)
    db.commit()
    db.refresh(novo_tipo_refeicao)
    return novo_tipo_refeicao


def update_tipo_refeicao(db: Session, tipo_refeicao_id: int, tipo_refeicao_data: TipoRefeicaoUpdate):
    tipo_refeicao = db.query(TipoRefeicao).filter(
        TipoRefeicao.id == tipo_refeicao_id
    ).first()

    if not tipo_refeicao:
        return None

    for key, value in tipo_refeicao_data.model_dump(exclude_unset=True).items():
        setattr(tipo_refeicao, key, value)

    db.commit()
    db.refresh(tipo_refeicao)
    return tipo_refeicao
