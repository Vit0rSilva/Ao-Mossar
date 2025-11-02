from sqlalchemy.orm import Session
from database.models.horario_models import Horario
from src.app.schemas.horario_schemas import HorarioCreate, HorarioUpdate
from database.repositories.tipoRefeicao_repositories import get_tipo_refeicao_nome
from database.repositories.usuario_repositories import get_usuario_numero

def get_horarios(db: Session):
    return db.query(Horario).all()


def get_horario(db: Session, horario_id: int):
    return db.query(Horario).filter(
        Horario.id == horario_id
    ).first()

def get_horarios_refeicao(usuario_numero:str, tipo_refeicao:str, db: Session):
    
    tipo_refeicao_obj = get_tipo_refeicao_nome(db, tipo_refeicao)
    usuario_obj = get_usuario_numero(db, usuario_numero)
    
    if not tipo_refeicao_obj or not usuario_obj:
        return None
        
    return db.query(Horario).filter(
        Horario.tipo_refeicao_id == tipo_refeicao_obj.id,
        Horario.usuario_id == usuario_obj.id
    ).first()

def get_horarios_usuario(usuario_numero:str, db: Session):
    
    usuario_obj = get_usuario_numero(db, usuario_numero)
    
    if not usuario_obj:
        return None
        
    return db.query(Horario).filter(
        Horario.usuario_id == usuario_obj.id
    )

def create_horario(db: Session, horario: HorarioCreate):
    novo_horario = Horario(**horario.model_dump())
    db.add(novo_horario)
    db.commit()
    db.refresh(novo_horario)
    return novo_horario


def update_horario(db: Session, horario_id: int, horario_data: HorarioUpdate):
    horario = db.query(Horario).filter(
        Horario.id == horario_id
    ).first()

    if not horario:
        return None

    for key, value in horario_data.model_dump(exclude_unset=True).items():
        setattr(horario, key, value)

    db.commit()
    db.refresh(horario)
    return horario
