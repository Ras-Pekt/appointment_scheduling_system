from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import hash_password
from deps.db import get_db
from models.user import User
from schemas.user import UserCreate
from deps.auth import get_current_admin
from deps.auth import get_current_doctor
from deps.auth import get_current_patient

Admin_Dependency = Annotated[User, Depends(get_current_admin)]
Doctor_Dependency = Annotated[User, Depends(get_current_doctor)]
Patient_Dependency = Annotated[User, Depends(get_current_patient)]

DB_Dependency = Annotated[Session, Depends(get_db)]


def create_user(user_data: dict, db: DB_Dependency) -> str:
    """
    Create a new user in the database.

    Args:
        user_data (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        str: The ID of the newly created user.
    """
    existing_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    try:
        new_user = User(
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            role=user_data.get("role"),
            hashed_password=hash_password(user_data.get("hashed_password")),
        )

        db.add(new_user)
        db.flush()
        db.refresh(new_user)
        db.commit()

        return new_user.id

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}",
        )
