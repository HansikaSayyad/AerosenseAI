# backend/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.repositories.user_repository import UserRepository
from backend.security.password_handler import password_handler
from backend.security.jwt_handler import jwt_handler
from backend.schemas.user import UserCreate, UserLogin


class UserService:
    """
    Handles all user business logic:
    - Registration with validation
    - Login with password verification
    - Profile management
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    # ─────────────────────────────────────────
    # REGISTER
    # ─────────────────────────────────────────
    def register(self, user_data: UserCreate) -> dict:
        """
        Registers a new user.

        Steps:
        1. Check email not already taken
        2. Check username not already taken
        3. Hash password
        4. Save to database
        5. Return tokens
        """

        # Check email
        if self.user_repo.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check username
        if self.user_repo.username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Hash password — never store plain text!
        hashed_password = password_handler.hash_password(user_data.password)

        # Create user
        user = self.user_repo.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )

        # Generate tokens
        tokens = jwt_handler.create_token_pair(
            user_id=str(user.id),
            role=user.role.value
        )

        return {
            "user": user,
            "tokens": tokens
        }

    # ─────────────────────────────────────────
    # LOGIN
    # ─────────────────────────────────────────
    def login(self, login_data: UserLogin) -> dict:
        """
        Logs in a user.

        Steps:
        1. Find user by email
        2. Verify password
        3. Check account is active
        4. Update last login
        5. Return tokens
        """

        # Find user
        user = self.user_repo.get_by_email(login_data.email)

        # Verify user exists and password is correct
        if not user or not password_handler.verify_password(
            login_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Check account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )

        # Update last login timestamp
        self.user_repo.update_last_login(user.id)

        # Generate tokens
        tokens = jwt_handler.create_token_pair(
            user_id=str(user.id),
            role=user.role.value
        )

        return {
            "user": user,
            "tokens": tokens
        }

    # ─────────────────────────────────────────
    # GET PROFILE
    # ─────────────────────────────────────────
    def get_profile(self, user_id: str):
        """Returns user profile by ID"""
        from uuid import UUID
        user = self.user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    # ─────────────────────────────────────────
    # REFRESH TOKEN
    # ─────────────────────────────────────────
    def refresh_token(self, refresh_token: str) -> dict:
        """Issues a new access token from a valid refresh token"""
        payload = jwt_handler.verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        new_access_token = jwt_handler.create_access_token(
            user_id=payload["sub"],
            role=payload.get("role", "user")
        )
        return {"access_token": new_access_token, "token_type": "bearer"}