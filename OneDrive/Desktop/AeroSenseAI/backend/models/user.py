# backend/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.connection import Base
import uuid
import enum


class UserRole(str, enum.Enum):
    """
    RBAC Roles:
    - ADMIN: full access
    - USER: standard access
    - PREMIUM: advanced features
    """
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    # ─────────────────────────────────────────
    # PRIMARY KEY — UUID instead of integer
    # More secure — can't guess next user ID
    # ─────────────────────────────────────────
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    # ─────────────────────────────────────────
    # USER FIELDS
    # ─────────────────────────────────────────
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    # ─────────────────────────────────────────
    # RBAC ROLE
    # ─────────────────────────────────────────
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    # ─────────────────────────────────────────
    # ACCOUNT STATUS
    # ─────────────────────────────────────────
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # ─────────────────────────────────────────
    # TIMESTAMPS
    # server_default = PostgreSQL sets the time
    # onupdate = auto updates on every change
    # ─────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # ─────────────────────────────────────────
    # RELATIONSHIPS
    # One user can have many locations
    # One user can have many recommendations
    # ─────────────────────────────────────────
    locations = relationship("Location", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"