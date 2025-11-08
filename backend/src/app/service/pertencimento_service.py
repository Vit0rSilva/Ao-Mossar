from sqlalchemy.orm import Session
from database.models import cardapio_models, horario_models

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