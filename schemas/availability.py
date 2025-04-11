from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import time

from core.enums import WeekdayEnum


class AvailabilityBase(BaseModel):
    doctor_id: str = Field(..., description="Doctor's ID")
    weekday: WeekdayEnum = Field(..., description="Day Available")
    start_time: time = Field(..., description="Availability start time")
    end_time: time = Field(
        ..., description="Availability end time (must be in the future)"
    )

    @field_validator("end_time")
    @classmethod
    def check_time_order(cls, end, info):
        start = info.data.get("start_time")
        if start and end <= start:
            raise ValueError("end_time must be after start_time")
        return end


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityOut(AvailabilityBase):
    id: str = Field(..., description="Availability's ID")
    available: bool = Field(..., description="Availability status")

    model_config = ConfigDict(from_attributes=True)


class AvailabilitySlotResponse(AvailabilityOut):
    pass

    model_config = ConfigDict(from_attributes=True)
