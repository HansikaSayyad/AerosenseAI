# backend/security/jwt_handler.py

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from backend.core.config import settings


class JWTHandler:
    """
    Handles all JWT token operations.

    Access Token  → short lived (30 mins) — used for API calls
    Refresh Token → long lived (7 days)  — used to get new access token
    """

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_expire = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_expire = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS

    # ─────────────────────────────────────────
    # CREATE TOKENS
    # ─────────────────────────────────────────
    def create_access_token(self, user_id: str, role: str) -> str:
        """Creates a short-lived access token"""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_expire
        )
        payload = {
            "sub": user_id,
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Creates a long-lived refresh token"""
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_expire
        )
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_token_pair(self, user_id: str, role: str) -> dict:
        """Creates both access and refresh tokens together"""
        return {
            "access_token": self.create_access_token(user_id, role),
            "refresh_token": self.create_refresh_token(user_id),
            "token_type": "bearer"
        }

    # ─────────────────────────────────────────
    # VERIFY TOKENS
    # ─────────────────────────────────────────
    def verify_access_token(self, token: str) -> Optional[dict]:
        """
        Verifies access token and returns payload.
        Returns None if token is invalid or expired.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            if payload.get("type") != "access":
                return None
            return payload
        except JWTError:
            return None

    def verify_refresh_token(self, token: str) -> Optional[dict]:
        """
        Verifies refresh token and returns payload.
        Returns None if token is invalid or expired.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            if payload.get("type") != "refresh":
                return None
            return payload
        except JWTError:
            return None

    def get_user_id_from_token(self, token: str) -> Optional[str]:
        """Extracts user_id from a valid token"""
        payload = self.verify_access_token(token)
        if payload:
            return payload.get("sub")
        return None


# Single instance to use everywhere
jwt_handler = JWTHandler()