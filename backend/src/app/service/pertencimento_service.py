from sqlalchemy.orm import Session
from database.models import cardapio_models, horario_models, alimento_models, cardapio_alimento_models, check_models


class PertencimentoService:
    def __init__(self, db: Session):
        self.db = db

    def verificar_pertecimento_cardapio(self, cardapio_id: int, usuario_id: str) -> bool:
        """Verifica se um Cardápio pertence ao usuário (via Horario)"""

        consulta = self.db.query(cardapio_models.Cardapio.id) \
            .join(horario_models.Horario, cardapio_models.Cardapio.horario_id == horario_models.Horario.id) \
            .filter(cardapio_models.Cardapio.id == cardapio_id) \
            .filter(horario_models.Horario.usuario_id == usuario_id) \
            .first()
        
        # Se a consulta achar algo, retorna True. Se for None, retorna False.
        return consulta is not None
    
    def verificar_pertecimento_horario(self, horario_id: int, usuario_id: str) -> bool:
        """Verifica se um Cardápio pertence ao usuário (via Horario)"""

        consulta = self.db.query(horario_models.Horario).filter(
            horario_models.Horario.id == horario_id
        ) \
        .filter(horario_models.Horario.usuario_id == usuario_id).first()
        
        # Se a consulta achar algo, retorna True. Se for None, retorna False.
        return consulta is not None
    
    def verificar_pertecimento_alimento(self, alimento_id: int, usuario_id: str) -> bool:
        """
        Verifica se um Alimento pertence a um usuário,
        seguindo a trilha: Alimento -> CardapioAlimento -> Cardapio -> Horario
        """

        consulta = self.db.query(alimento_models.Alimento.id) \
            .join(
                cardapio_alimento_models.CardapioAlimento,
                alimento_models.Alimento.id == cardapio_alimento_models.CardapioAlimento.alimento_id
            ) \
            .join(
                cardapio_models.Cardapio,
                cardapio_alimento_models.CardapioAlimento.cardapio_id == cardapio_models.Cardapio.id
            ) \
            .join(
                horario_models.Horario,
                cardapio_models.Cardapio.horario_id == horario_models.Horario.id
            ) \
            .filter(
                alimento_models.Alimento.id == alimento_id  # 1. Filtra pelo alimento certo
            ) \
            .filter(
                horario_models.Horario.usuario_id == usuario_id  # 2. Filtra pelo usuário certo
            ) \
            .first()
        
        return consulta is not None
    
    def verificar_pertecimento_check(self, check_id: int, usuario_id: str) -> bool:

        consulta = self.db.query(check_models.Check).filter(
            check_models.Check.id == check_id
        ) \
        .filter(horario_models.Horario.usuario_id == usuario_id).first()

        # Se a consulta achar algo, retorna True. Se for None, retorna False.
        return consulta is not None
    
    def verificar_pertecimento_id(api_id:str, id_usuario: str) -> bool:
        if api_id == id_usuario:
            return True
        return False