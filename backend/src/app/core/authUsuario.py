# app/service/authUsuario.py
from fastapi import HTTPException, status
from app.schemas.usuario_schemas import UsuarioCreate, UsuarioOut
from app.core.security import hash_password
from app.core.jwt_handler import create_access_token
from app.repositories.usuario_repositories import UsuarioRepository

def create_usuario_service(payload: UsuarioCreate, repo: UsuarioRepository):
    if repo.get_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email já cadastrado", "error_code": "EMAIL_EXISTS"}
        )

    if repo.get_by_cpf(payload.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "CPF já cadastrado", "error_code": "CPF_EXISTS"}
        )

    hashed = hash_password(payload.senha)
    usuario = repo.create(payload, hashed_password=hashed)

    token_data = create_access_token(subject=usuario.id)

    out = UsuarioOut.model_validate(usuario)

    return {
        **out.model_dump(mode="json"),
        "access_token": token_data["access_token"],
        "expires_in": token_data["expires_in"]
    }