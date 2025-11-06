from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.schemas import usuario_schemas, response_schemas
from database.repositories import usuario_repositories
from src.app.deps import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_usuarios(db: Session = Depends(get_db)):
    usuario = usuario_repositories.get_usuarios(db)

    usuario_data = [
        usuario_schemas.UsuarioResponse.model_validate(tr).model_dump()
        for tr in usuario
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os tipos de usuario.",
        data=usuario_data
    )


@router.get("/{usuario_id}", response_model=response_schemas.SuccessResponse)
def usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_repositories.get_usuario(db, usuario_id)
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


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_usuario(
    usuario: usuario_schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    if not usuario:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_usuario = usuario_repositories.create_usuario(db, usuario)

    return response_schemas.SuccessResponse(
        message="Usuario criado com sucesso.",
        data=usuario_schemas.UsuarioResponse.model_validate(novo_usuario)
    )


@router.put("/{usuario_id}", response_model=response_schemas.SuccessResponse)
def atualizar_usuario(
    usuario_id: int,
    usuario_data: usuario_schemas.UsuarioUpdate,
    db: Session = Depends(get_db)
):
    usuario_atualizado = usuario_repositories.update_usuario(
        db, usuario_id, usuario_data
    )

    if not usuario_atualizado:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Usuario não encontrado",
                "error_code": "NOT_FOUND_USUARIO"
            }
        )

    return response_schemas.SuccessResponse(
        message="Usuario atualizado com sucesso.",
        data=usuario_schemas.UsuarioResponse.model_validate(usuario_atualizado)
    )


@router.delete("/{usuario_id}", response_model=response_schemas.SuccessResponse)
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = usuario_repositories.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Usuario não encontrado",
                "error_code": "NOT_FOUND_USUARIO"
            }
        )

    db.delete(usuario)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Usuario deletado com sucesso.",
        data=False
    )

@router.post("/login", response_model=SuccessResponse)
def login(payload: UsuarioLogin, repo: UsuarioRepository = Depends(get_usuario_repo)):
    usuario = repo.get_by_email(payload.email)
    if not usuario or not verify_password(payload.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Email ou senha inválidos", "error_code": "EMAIL_SENHA_FALSE"}, headers={"WWW-Authenticate": "Bearer"})
    token_data = create_access_token(subject=usuario.id)
    return SuccessResponse(message="Login realizado com sucesso", data={"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]})

@router.get("/me", response_model=SuccessResponse)
def me(current_user = Depends(get_current_usuario)):
    data_user = UsuarioOut.model_validate(current_user).model_dump()
    return SuccessResponse(message="Usuário autenticado", data=data_user)