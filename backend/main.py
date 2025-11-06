from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from database.database import Base, engine
import database.models
from src.app.api import  tipo_refeicao, horario, usuario, cardapio, alimento, check
from src.app.middlewares.error_handler import (
    http_exception_handler,
    validation_error_handler,
    generic_exception_handler,
)

app = FastAPI(title="Aomossar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra handlers para EXCEÇÕES específicas (substitui o comportamento padrão)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)  # opcional, para erros inesperados

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# Registra rotas
app.include_router(tipo_refeicao.router)
app.include_router(horario.router)
app.include_router(usuario.router)
app.include_router(cardapio.router)
app.include_router(alimento.router)
app.include_router(check.router)