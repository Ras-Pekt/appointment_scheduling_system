from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password.

    Args:
        plain_password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """
    Create an access token.

    Args:
        data (dict): The data to include in the token.

    Returns:
        str: The access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
