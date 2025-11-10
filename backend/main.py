from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

# from fastapi_limiter import FastAPILimiter
# import redis.asyncio as redis

from src.app.schemas import horario_schemas, cardapio_schemas, cardapio_alimento_schemas
from database.database import Base, engine
# import database.models # Não costuma ser necessário se você já importa os modelos nos repositories/apis, mas mal não faz.
from src.app.api import tipo_refeicao, horario, usuario, cardapio, alimento, check, admin
from src.app.middlewares.error_handler import (
    http_exception_handler,
    validation_error_handler,
    generic_exception_handler,
)

# ==================================================================
# 👇 CORREÇÃO AQUI: REORDENANDO OS REBUILDS
# ==================================================================
# Precisamos seguir a ordem de dependência:
# 1. CardapioAlimento (não depende de ninguém)
cardapio_alimento_schemas.CardapioAlimentoResponse.model_rebuild()
# 2. Cardapio (depende de CardapioAlimento)
cardapio_schemas.CardapioResponse.model_rebuild()
# 3. Horario (depende de Cardapio)
horario_schemas.HorarioResponse.model_rebuild()
# ==================================================================

app = FastAPI(title="Aomossar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
# 👇 TUDO COMENTADO AQUI COMO VOCÊ PEDIU
@app.on_event("startup")
async def startup():
    # Função que é executada quando o FastAPI inicia.
    # 1. Define a conexão com o seu Redis (que está rodando no localhost)
    # redis_connection = redis.from_url(
    #     "redis://localhost:6379", 
    #     encoding="utf-8", 
    #     decode_responses=True
    # )
    
    # 2. "Liga" o fastapi-limiter com essa conexão
    # await FastAPILimiter.init(redis_connection)
    # print("FastAPILimiter 'ligado' e conectado ao Redis.")
    pass # 'pass' é necessário para a função não ficar vazia se tudo estiver comentado
"""

# Registra handlers para EXCEÇÕES específicas
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# Registra rotas
app.include_router(tipo_refeicao.router)
app.include_router(horario.router)
app.include_router(usuario.router)
app.include_router(cardapio.router)
app.include_router(alimento.router)
app.include_router(check.router)
app.include_router(admin.router)