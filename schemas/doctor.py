from typing import List
from pydantic import BaseModel, ConfigDict, Field
from schemas.availability import AvailabilitySlotResponse
from schemas.user import UserCreate, UserOut


class DoctorBase(BaseModel):
    specialization: str = Field(
        ..., min_length=2, max_length=100, description="Doctor's specialization"
    )


class DoctorCreate(UserCreate, DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: str = Field(..., description="Doctor's ID")
    availability: List[AvailabilitySlotResponse]
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
