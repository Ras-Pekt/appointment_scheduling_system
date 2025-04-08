from pydantic import BaseModel, Field
from schemas.user import UserOut


class PatientBase(BaseModel):
    insurance_provider: str = Field(
        ..., min_length=2, max_length=50, description="Patient's insurance provider"
    )
    insurance_number: str = Field(
        ..., min_length=2, max_length=50, description="Patient's insurance number"
    )


class PatientCreate(PatientBase):
    user_id: str = Field(..., description="Patient's ID")


class PatientOut(PatientBase):
    id: str = Field(..., description="Patient's ID")
    user: UserOut

    class Config:
        orm_mode = True
