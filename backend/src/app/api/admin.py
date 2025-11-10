from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.app.schemas import admin_schemas, response_schemas
from database.repositories.admin_repositories import AdminRepository
from src.app.deps import get_db, get_admin_repo, get_current_admin
from src.app.core.security import verify_password
from src.app.core.jwt_handler import create_access_token
from src.app.core.authAdmin import create_admin_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.get("/{admin_id}", response_model=response_schemas.SuccessResponse)
def admin_por_id(admin_id: int, repo: AdminRepository = Depends(get_admin_repo), current_user = Depends(get_current_admin)):
    admin = repo.get_admin(admin_id)
    if not admin:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Admin não encontrado",
                "error_code": "NOT_FOUND_USUARIO"
            }
        )

    admin_data = admin_schemas.AdminResponse.model_validate(admin).model_dump()

    return response_schemas.SuccessResponse(
        message="Admin encontrado.",
        data=admin_data
    )

@router.post("/login", response_model=response_schemas.SuccessResponse)
def login(
        payload: admin_schemas.AdminLogin, 
        repo: AdminRepository = Depends(get_admin_repo),
        #limiter: RateLimiter = Depends(RateLimiter(times=2, minutes=120))        
    ):
    admin = repo.get_by_email(payload.email)
    if not admin or not verify_password(payload.senha, admin.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Email ou senha inválidos", "error_code": "EMAIL_SENHA_FALSE"}, headers={"WWW-Authenticate": "Bearer"})
    token_data = create_access_token(subject=admin.id)
    return response_schemas.SuccessResponse(message="Login realizado com sucesso", data={"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]})

@router.get("/me", response_model=response_schemas.SuccessResponse)
def me(current_user = Depends(get_current_admin)):
    data_user = admin_schemas.AdminOut.model_validate(current_user).model_dump()
    return response_schemas.SuccessResponse(message="Usuário autenticado", data=data_user)

