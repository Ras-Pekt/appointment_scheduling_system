from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from core.enums import WeekdayEnum


class AppointmentBase(BaseModel):
    doctor_id: str = Field(..., description="Doctor's ID")
    scheduled_start: datetime = Field(..., description="Start of the appointment")
    scheduled_end: datetime = Field(..., description="End of the appointment")
    status: str = Field(..., description="Appointment status")


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: str = Field(..., description="Appointment's ID")

    model_config = ConfigDict(from_attributes=True)
