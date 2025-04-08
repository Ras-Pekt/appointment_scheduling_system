from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone

from deps.utils import generate_uuid


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    doctor_id = Column(String(length=36), ForeignKey("doctors.id", ondelete="SET NULL"))
    patient_id = Column(
        String(length=36), ForeignKey("patients.id", ondelete="CASCADE")
    )
    appointment_id = Column(
        String(length=36), ForeignKey("appointments.id", ondelete="SET NULL")
    )
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    doctor = relationship("Doctor", back_populates="medical_records")
    patient = relationship("Patient", back_populates="medical_records")
    appointment = relationship("Appointment", back_populates="medical_record")
