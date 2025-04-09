from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from deps.db import get_db
from models.user import User
from schemas.user import UserCreate

DB_Dependency = Annotated[Session, Depends(get_db)]


def create_user(user_data: UserCreate, db: DB_Dependency) -> str:
    """
    Create a new user in the database.

    Args:
        user_data (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        str: The ID of the newly created user.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    try:
        new_user = User(**user_data)

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
