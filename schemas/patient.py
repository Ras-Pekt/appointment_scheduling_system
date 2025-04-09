from pydantic import BaseModel, ConfigDict, Field
from schemas.user import UserCreate, UserOut


class PatientBase(BaseModel):
    insurance_provider: str = Field(
        ..., min_length=2, max_length=50, description="Patient's insurance provider"
    )
    insurance_number: str = Field(
        ..., min_length=2, max_length=50, description="Patient's insurance number"
    )


class PatientCreate(UserCreate, PatientBase):
    pass


class PatientOut(PatientBase):
    id: str = Field(..., description="Patient's ID")
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
