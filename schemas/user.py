from pydantic import BaseModel, ConfigDict, EmailStr, Field
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
    hashed_password: str = Field(..., min_length=8, description="User's password")


class AdminOut(UserBase):
    id: str = Field(..., description="Admin's ID")

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: str = Field(..., description="User's ID")
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="User's last name"
    )

    model_config = ConfigDict(from_attributes=True)
