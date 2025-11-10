from sqlalchemy.orm import Session
from database.models.check_models import Check
from src.app.schemas.check_schemas import CheckCreate, CheckUpdate
from src.app.service.pertencimento_service import PertencimentoService

def get_checks(db: Session):
    return db.query(Check).all()


def get_check(db: Session, check_id: int):
    return db.query(Check).filter(
        Check.id == check_id
    ).first()

def get_checks_usuario(db:Session, usuario_id:set):
    return db.query(Check).filter(
        Check.usuario_id == usuario_id
    ).first()

def create_check(db: Session, check: CheckCreate, usuario_id: str):
    novo_check = Check(**check.model_dump())
    if not PertencimentoService.verificar_pertecimento_id(check.usuario_id, usuario_id): return False
    
    db.add(novo_check)
    db.commit()
    db.refresh(novo_check)
    return novo_check


def update_check(db: Session, check_id: int, check_data: CheckUpdate):
    check = db.query(Check).filter(
        Check.id == check_id
    ).first()

    if not check:
        return None

    for key, value in check_data.model_dump(exclude_unset=True).items():
        setattr(check, key, value)

    db.commit()
    db.refresh(check)
    return check
