# backend/repositories/user_repository.py

from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from backend.models.user import User, UserRole


class UserRepository:
    """
    Handles all database operations for Users.
    Never contains business logic — only DB queries.
    """

    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        role: UserRole = UserRole.USER
    ) -> User:
        """Creates a new user in database"""
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Finds user by UUID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Finds user by email — used for login"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Finds user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Returns all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────
    def update(self, user_id: UUID, **kwargs) -> Optional[User]:
        """Updates user fields"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user_id: UUID) -> None:
        """Updates last login timestamp"""
        from datetime import datetime, timezone
        self.update(user_id, last_login=datetime.now(timezone.utc))

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, user_id: UUID) -> bool:
        """Deletes user from database"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    # ─────────────────────────────────────────
    # CHECKS
    # ─────────────────────────────────────────
    def email_exists(self, email: str) -> bool:
        """Checks if email is already registered"""
        return self.db.query(User).filter(User.email == email).first() is not None

    def username_exists(self, username: str) -> bool:
        """Checks if username is already taken"""
        return self.db.query(User).filter(User.username == username).first() is not None