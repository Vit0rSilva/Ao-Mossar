from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.app.schemas import usuario_schemas, response_schemas
from database.repositories.usuario_repositories import UsuarioRepository
from src.app.deps import get_db, get_usuario_repo, get_current_usuario, get_current_admin
from src.app.core.security import verify_password
from src.app.core.jwt_handler import create_access_token
from src.app.core.authUsuario import create_usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/{usuario_id}", response_model=response_schemas.SuccessResponse)
def usuario_por_id(usuario_id: int, repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_admin)):
    usuario = repo.get_usuario(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Usuario não encontrado",
                "error_code": "NOT_FOUND_USUARIO"
            }
        )

    usuario_data = usuario_schemas.UsuarioResponse.model_validate(usuario).model_dump()

    return response_schemas.SuccessResponse(
        message="Usuario encontrado.",
        data=usuario_data
    )


@router.post("", response_model=response_schemas.SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    payload: usuario_schemas.UsuarioCreate,
    repo: UsuarioRepository = Depends(get_usuario_repo),
    #limiter: RateLimiter = Depends(RateLimiter(times=1, minutes=60))
):
    content = create_usuario_service(payload, repo)
    return response_schemas.SuccessResponse(message="Usuário criado com sucesso", data=content)

@router.post("/login", response_model=response_schemas.SuccessResponse)
def login(payload: usuario_schemas.UsuarioLogin, repo: UsuarioRepository = Depends(get_usuario_repo), 
          #limiter: RateLimiter = Depends(RateLimiter(times=10, minutes=15))
        ):
    usuario = repo.get_by_email(payload.email)
    if not usuario or not verify_password(payload.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Email ou senha inválidos", "error_code": "EMAIL_SENHA_FALSE"}, headers={"WWW-Authenticate": "Bearer"})
    token_data = create_access_token(subject=usuario.id)
    return response_schemas.SuccessResponse(message="Login realizado com sucesso", data={"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]})

@router.get("/me", response_model=response_schemas.SuccessResponse)
def me(current_user = Depends(get_current_usuario), 
       #limiter: RateLimiter = Depends(RateLimiter(times=20, minutes=5))
       ):
    data_user = usuario_schemas.UsuarioOut.model_validate(current_user).model_dump()
    return response_schemas.SuccessResponse(message="Usuário autenticado", data=data_user)

