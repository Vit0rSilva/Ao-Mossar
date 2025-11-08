# /backend/seed_admin.py

import sys
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
load_dotenv()

# --- Configuração de Logging ---
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    from database.database import SessionLocal  # Onde você define sua sessão
    from src.app.schemas import admin_schemas    # Onde está seu AdminCreate
    from database.repositories.admin_repositories import AdminRepository # Onde está seu Repo
    from src.app.core.authAdmin import create_admin_service # Onde está seu Service
    
except ImportError as e:
    log.error(f"Erro de importação: {e}")
    log.error("Verifique se você está rodando este script da pasta 'backend/'")
    log.error("E verifique se os caminhos de importação acima estão corretos.")
    sys.exit(1)


# --- Dados do Admin a ser Criado ---
# ‼️ Altere estes dados para o seu admin principal
ADMIN_PAYLOAD = admin_schemas.AdminCreate(
    email="adminvss@aomossar.com",
    senha="t4z9DY49Xa5w0XXQjI4dR8SDbJYU1X!",
    nome="Administrador Principal",
    telefone="5571991366331"
    # Adicione outros campos se o seu AdminCreate exigir (ex: 'telefone')
)


def seed_admin():
    """
    Função principal do seeder.
    """
    log.info("Iniciando o seeder para criar o admin principal...")
    db = None
    try:
        # 1. Criar uma sessão de banco de dados
        db = SessionLocal()
        log.info("Conexão com o banco de dados estabelecida.")

        # 2. Instanciar o repositório
        repo = AdminRepository(db=db)

        # 3. Chamar o serviço (reutilizando sua lógica de negócios)
        log.info(f"Tentando criar o admin: {ADMIN_PAYLOAD.email}")
        
        # Esta é a mesma função que sua API chama.
        # Ela vai lidar com o hash da senha e a verificação de e-mail duplicado.
        content = create_admin_service(payload=ADMIN_PAYLOAD, repo=repo)
        
        log.info("---------------------------------")
        log.info("✅ Administrador criado com sucesso! ✅")
        log.info(f"   Email: {content.get('email', 'N/A')}")
        log.info(f"   Nome: {content.get('nome', 'N/A')}")
        log.info("---------------------------------")

    except HTTPException as e:
        # Captura erros do seu serviço (ex: "Email já cadastrado")
        log.error("---------------------------------")
        log.error(f"❌ ERRO (HTTPException): {e.detail}")
        log.error("---------------------------------")
    except Exception as e:
        # Captura outros erros (ex: falha na conexão com o banco)
        log.error("---------------------------------")
        log.error(f"❌ ERRO INESPERADO: {e}")
        log.error("---------------------------------")
        if db:
            db.rollback() # Desfaz qualquer transação parcial em caso de erro
    finally:
        # 4. Fechar a sessão do banco
        if db:
            db.close()
            log.info("Conexão com o banco de dados fechada.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    seed_admin()