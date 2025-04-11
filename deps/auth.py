from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .db import get_db
from models import User
from schemas.user import UserRole
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Get the current user based on the provided token.

    Args:
        token (str): The JWT token.
        db (Session): The database session.

    Returns:
        User: The current user.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = str(payload.get("sub"))

        print("FROM GET CURRENT USER: ", user_id)

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def require_role(required_role: UserRole):
    """
    Decorator to require a specific user role.

    Args:
        required_role (UserRole): The required user role.

    Returns:
        Callable: The decorated function.
    """

    def role_dependency(user: Annotated[User, Depends(get_current_user)]):
        """
        Decorator to require a specific user role.

        Args:
            user (User): The current user.

        Returns:
            User: The current user.
        """
        if user.role != required_role:
            raise HTTPException(
                status_code=403, detail="You do not have access to this resource"
            )
        return user

    return role_dependency


# Specific role dependencies
get_current_admin = require_role(UserRole.admin)
get_current_doctor = require_role(UserRole.doctor)
get_current_patient = require_role(UserRole.patient)
