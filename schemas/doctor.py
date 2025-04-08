from pydantic import BaseModel, Field
from schemas.user import UserOut


class DoctorBase(BaseModel):
    specialization: str = Field(
        ..., min_length=2, max_length=100, description="Doctor's specialization"
    )


class DoctorCreate(DoctorBase):
    user_id: str = Field(..., description="Doctor's ID")


class DoctorOut(DoctorBase):
    id: str = Field(..., description="Doctor's ID")
    user: UserOut

    class Config:
        orm_mode = True
