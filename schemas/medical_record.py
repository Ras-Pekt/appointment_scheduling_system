from pydantic import BaseModel, Field
from typing import Optional


class MedicalRecordBase(BaseModel):
    patient_id: str = Field(..., description="Patient's ID")
    doctor_id: str = Field(..., description="Doctor's ID")
    appointment_id: str = Field(..., description="Appointment's ID")
    notes: Optional[str] = Field(None, description="Doctor's Medical notes")


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordOut(MedicalRecordBase):
    id: str = Field(..., description="Medical record's ID")

    class Config:
        orm_mode = True
