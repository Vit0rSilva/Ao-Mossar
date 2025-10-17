from sqlalchemy.orm import Session
from database.models.horario_models import Horario
from src.app.schemas.horario_schemas import HorarioCreate, HorarioUpdate

def get_horarios(db: Session):
    return db.query(Horario).all()


def get_horario(db: Session, horario_id: int):
    return db.query(Horario).filter(
        Horario.id == horario_id
    ).first()


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
