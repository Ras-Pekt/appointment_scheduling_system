from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="SET NULL"))
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="SET NULL"))
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    doctor = relationship("Doctor", back_populates="medical_records")
    patient = relationship("Patient", back_populates="medical_records")
    appointment = relationship("Appointment", back_populates="medical_record")
