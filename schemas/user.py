from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="User's last name"
    )
    role: UserRole = Field(..., description="User's role")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password")


class UserOut(UserBase):
    id: str = Field(..., description="User's ID")

    class Config:
        orm_mode = True
