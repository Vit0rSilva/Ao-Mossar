from fastapi import Depends
from sqlalchemy.orm import Session
from database.models.horario_models import Horario
from database.models.cardapio_models import Cardapio
from src.app.schemas.horario_schemas import HorarioCreate, HorarioUpdate
from database.repositories.tipoRefeicao_repositories import get_tipo_refeicao_nome
from src.app.deps import get_db, get_usuario_repo, get_current_usuario
from database.repositories.usuario_repositories import UsuarioRepository
from src.app.service.pertencimento_service import PertencimentoService

def get_horarios(db: Session):
    return db.query(Horario).all()


def get_horario(db: Session, horario_id: int):
    return db.query(Horario).filter(
        Horario.id == horario_id
    ).first()

def get_horarios_refeicao(usuario_numero:str, tipo_refeicao:str,db:Session):
    repo: UsuarioRepository = Depends(get_usuario_repo)
    
    tipo_refeicao_obj = get_tipo_refeicao_nome(db, tipo_refeicao)
    usuario_obj = repo.get_usuario_numero(usuario_numero)
    
    if not tipo_refeicao_obj or not usuario_obj:
        return None
        
    return db.query(Horario).filter(
        Horario.tipo_refeicao_id == tipo_refeicao_obj.id,
        Horario.usuario_id == usuario_obj.id
    ).first()

def get_cardapio_usuario(usuario_numero: str, db: Session):
    """
    Busca TODOS os horários de um usuário e, para cada horário,
    anexa sua lista de cardápios (que pode ser vazia).
    """
    
    horarios = get_horarios_usuario(usuario_numero, db) 

    if not horarios:
        return []

    horario_ids = [horario.id for horario in horarios]
    
    cardapios_do_usuario = db.query(Cardapio).filter(
        Cardapio.horario_id.in_(horario_ids)
    ).all()

    cardapios_map = {}
    for c in cardapios_do_usuario:
        if c.horario_id not in cardapios_map:
            cardapios_map[c.horario_id] = []
        cardapios_map[c.horario_id].append(c)

    for h in horarios:
        h.cardapios = cardapios_map.get(h.id, []) 

    return horarios

def get_horarios_usuario(usuario_numero: str, db: Session):
    """Busca todos os horários de um usuário"""

    pertencimento_service = UsuarioRepository(db=db)
    usuario_obj = pertencimento_service.get_usuario_numero(usuario_numero)
    
    if not usuario_obj:
        return None
        
    return db.query(Horario).filter(
        Horario.usuario_id == usuario_obj.id
    ).all()


def create_horario(db: Session, horario: HorarioCreate, usuario_id):
    if not PertencimentoService.verificar_pertecimento_id(horario.usuario_id, usuario_id): return False
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
