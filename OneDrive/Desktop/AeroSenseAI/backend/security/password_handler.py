# backend/security/password_handler.py

from passlib.context import CryptContext

# ─────────────────────────────────────────
# PASSWORD CONTEXT
# bcrypt is the industry standard
# auto = automatically uses best algorithm
# ─────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHandler:
    """
    Handles all password operations.
    Never stores or returns plain passwords.
    """

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Converts plain password to bcrypt hash.

        Example:
            "MyPass123" → "$2b$12$xyz..."
        """
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies plain password against stored hash.

        Example:
            verify("MyPass123", "$2b$12$xyz...") → True
            verify("WrongPass", "$2b$12$xyz...") → False
        """
        return pwd_context.verify(plain_password, hashed_password)


# Single instance to use everywhere
password_handler = PasswordHandler()