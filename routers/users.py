from fastapi import APIRouter
from models.user import User
from routers import DB_Dependency

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


from pydantic import BaseModel


class UserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str


@users_router.get("/")
async def get_users():
    print("Get all users")
    return {"message": "Get all users"}


@users_router.post("/new-user")
async def register_new_user(user_data: UserRequest, db: DB_Dependency):
    print("USER DATA: ", user_data)
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully", "new_user": new_user}
