from pydantic import BaseModel, Field
from datetime import datetime


class AppointmentBase(BaseModel):
    patient_id: str = Field(..., description="Patient's ID")
    doctor_id: str = Field(..., description="Doctor's ID")
    scheduled_time: datetime = Field(..., description="Scheduled appointment time")
    status: str = Field(..., description="Appointment status")


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: str = Field(..., description="Appointment's ID")

    class Config:
        orm_mode = True
