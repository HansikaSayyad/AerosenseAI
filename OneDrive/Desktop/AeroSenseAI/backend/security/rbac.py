# backend/security/rbac.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.security.jwt_handler import jwt_handler
from backend.models.user import UserRole

# ─────────────────────────────────────────
# HTTP BEARER SCHEME
# ─────────────────────────────────────────
bearer_scheme = HTTPBearer()
bearer_scheme_optional = HTTPBearer(auto_error=False)


class RBACHandler:
    """
    Role-Based Access Control.

    Usage in routes:
        # Any logged in user:
        @router.get("/", dependencies=[Depends(rbac.require_auth)])

        # Admin only:
        @router.get("/", dependencies=[Depends(rbac.require_admin)])
    """

    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> dict:
        """
        Extracts and validates current user from JWT token.
        Raises 401 if token is invalid.
        """
        token = credentials.credentials
        payload = jwt_handler.verify_access_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return payload

    def require_auth(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> dict:
        """Requires any authenticated user"""
        return self.get_current_user(credentials)

    def optional_auth(
        self,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme_optional)
    ) -> Optional[dict]:
        """Returns user payload if token present, None otherwise — never raises"""
        if not credentials:
            return None
        try:
            payload = jwt_handler.verify_access_token(credentials.credentials)
            return payload
        except Exception:
            return None

    def require_admin(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> dict:
        """Requires admin role"""
        payload = self.get_current_user(credentials)
        if payload.get("role") != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return payload

    def require_premium(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ) -> dict:
        """Requires premium or admin role"""
        payload = self.get_current_user(credentials)
        allowed = [UserRole.PREMIUM.value, UserRole.ADMIN.value]
        if payload.get("role") not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium access required"
            )
        return payload


# Single instance to use everywhere
rbac = RBACHandler()