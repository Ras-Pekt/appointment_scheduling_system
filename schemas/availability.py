from pydantic import BaseModel, Field
from datetime import datetime


class AvailabilityBase(BaseModel):
    doctor_id: str = Field(..., description="Doctor's ID")
    weekday: str = Field(..., description="Day Available")
    start_time: datetime = Field(..., description="Availability start time")
    end_time: datetime = Field(
        ..., description="Availability end time (must be in the future)"
    )


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityOut(AvailabilityBase):
    id: str = Field(..., description="Availability's ID")

    class Config:
        orm_mode = True
