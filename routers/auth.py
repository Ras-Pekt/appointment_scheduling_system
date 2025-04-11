from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password, create_access_token
from models import User
from routers import DB_Dependency
from schemas.auth import Token
from starlette import status

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DB_Dependency,
):
    """
    Login a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (DB_Dependency): The database dependency.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
