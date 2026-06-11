# backend/schemas/user.py

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from backend.models.user import UserRole


# ─────────────────────────────────────────
# BASE SCHEMA — shared fields
# ─────────────────────────────────────────
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


# ─────────────────────────────────────────
# CREATE SCHEMA — used when registering
# ─────────────────────────────────────────
class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum():
            raise ValueError("Username must contain only letters and numbers")
        return v


# ─────────────────────────────────────────
# RESPONSE SCHEMA — returned to frontend
# Never includes password!
# ─────────────────────────────────────────
class UserResponse(UserBase):
    id: UUID
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# UPDATE SCHEMA — used when editing profile
# All fields optional
# ─────────────────────────────────────────
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# ─────────────────────────────────────────
# LOGIN SCHEMA
# ─────────────────────────────────────────
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ─────────────────────────────────────────
# TOKEN SCHEMAS
# ─────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None