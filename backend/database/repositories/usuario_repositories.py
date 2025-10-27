from sqlalchemy.orm import Session
from database.models.usuario_models import Usuario
from src.app.schemas.usuario_schemas import UsuarioCreate, UsuarioUpdate

def get_usuarios(db: Session):
    return db.query(Usuario).all()


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

def get_usuario_numero(db: Session, numero: str):
    return db.query(Usuario).filter(
        Usuario.telefone == numero
    ).first()


def create_usuario(db: Session, usuario: UsuarioCreate):
    novo_usuario = Usuario(**usuario.model_dump())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        return None

    for key, value in usuario_data.model_dump(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario
