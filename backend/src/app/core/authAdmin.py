# app/service/authAdmin.py
from fastapi import HTTPException, status
from src.app.schemas.admin_schemas import AdminCreate, AdminOut
from src.app.core.security import hash_password
from src.app.core.jwt_handler import create_access_token
from database.repositories.admin_repositories import AdminRepository

def create_admin_service(payload: AdminCreate, repo: AdminRepository):
    if repo.get_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email já cadastrado", "error_code": "EMAIL_EXISTS"}
        )

    hashed = hash_password(payload.senha)
    admin = repo.create(payload, hashed_password=hashed)

    token_data = create_access_token(subject=admin.id)

    out = AdminOut.model_validate(admin)

    return {
        **out.model_dump(mode="json"),
        "access_token": token_data["access_token"],
        "expires_in": token_data["expires_in"]
    }