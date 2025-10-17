from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.app.schemas.response_schemas import ErrorResponse
import traceback

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Substitui o comportamento padrão do FastAPI para HTTPException
    e sempre retorna o formato padronizado ErrorResponse.
    """
    # exc.detail pode ser dict ou string; trate ambos
    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", str(exc.detail))
        error_code = exc.detail.get("error_code")
    else:
        message = str(exc.detail)
        error_code = None

    content = ErrorResponse(
        success=False,
        message=message,
        error_code=error_code,
        data=None
    ).model_dump()

    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Transforma validações Pydantic/RequestValidationError no formato padronizado.
    """
    erros = []
    for err in exc.errors():
        erros.append({
            "campo": " → ".join(map(str, err["loc"])),
            "mensagem": err["msg"],
            "tipo": err["type"],
            "valor_enviado": err.get("input")
        })

    content = ErrorResponse(
        success=False,
        message="Erro de validação nos dados enviados.",
        error_code="VALIDATION_ERROR",
        data={"erros": erros}
    ).model_dump()

    return JSONResponse(status_code=422, content=content)


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all: em caso de erro inesperado, retorna o formato padronizado.
    (Você pode logar/traceback aqui conforme precisar.)
    """
    # Opcional: log mais detalhado
    traceback.print_exc()

    content = ErrorResponse(
        success=False,
        message="Erro inesperado no servidor.",
        error_code="UNEXPECTED_ERROR",
        data=None
    ).model_dump()

    return JSONResponse(status_code=500, content=content)
