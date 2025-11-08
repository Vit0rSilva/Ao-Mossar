from dotenv import load_dotenv
load_dotenv()

# 1. Importe seu serviço E sua sessão do banco
from backend.src.app.service.pertencimento_service import AlimentoService
from database.database import SessionLocal  # <-- Importe o SessionLocal

# 2. Crie uma sessão do banco manualmente
db = SessionLocal()

# 3. Crie a instância do serviço manualmente, passando o 'db'
repo = AlimentoService(db=db)

try:
    print("Tentando buscar o cardápio...")
    # 4. Chame sua função
    resultado = repo.verificar_pertecimento_cardapio(cardapioURL=4)
    print(f"Resultado: {resultado}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    # 5. SEMPRE feche a sessão do banco
    db.close()
    print("Conexão fechada.")