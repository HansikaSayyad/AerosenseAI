# backend/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.services.user_service import UserService
from backend.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token
)
from backend.security.rbac import rbac
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ─────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────
@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - Validates email and username uniqueness
    - Hashes password securely
    - Returns JWT tokens
    """
    service = UserService(db)
    result = service.register(user_data)

    return {
        "success": True,
        "message": "Registration successful",
        "user": {
            "id": str(result["user"].id),
            "email": result["user"].email,
            "username": result["user"].username,
            "role": result["user"].role.value
        },
        "tokens": result["tokens"]
    }


# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
@router.post("/login", response_model=dict)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.

    - Verifies credentials
    - Returns JWT access and refresh tokens
    """
    service = UserService(db)
    result = service.login(login_data)

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "id": str(result["user"].id),
            "email": result["user"].email,
            "username": result["user"].username,
            "role": result["user"].role.value
        },
        "tokens": result["tokens"]
    }


# ─────────────────────────────────────────
# GET MY PROFILE
# ─────────────────────────────────────────
@router.get("/me", response_model=dict)
async def get_my_profile(
    current_user: dict = Depends(rbac.require_auth),
    db: Session = Depends(get_db)
):
    """
    Get current logged-in user profile.
    Requires valid JWT token.
    """
    service = UserService(db)
    user = service.get_profile(current_user["sub"])

    return {
        "success": True,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": str(user.created_at)
        }
    }


# ─────────────────────────────────────────
# REFRESH TOKEN
# ─────────────────────────────────────────
class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token.
    """
    service = UserService(db)
    result = service.refresh_token(request.refresh_token)

    return {
        "success": True,
        "access_token": result["access_token"],
        "token_type": "bearer"
    }