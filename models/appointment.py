from sqlalchemy import Column, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship
from core.database import Base
from core.enums import AppointmentStatusEnum
from deps.utils import generate_uuid


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    doctor_id = Column(String(length=36), ForeignKey("doctors.id", ondelete="CASCADE"))
    patient_id = Column(
        String(length=36), ForeignKey("patients.id", ondelete="CASCADE")
    )
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(
        Enum(AppointmentStatusEnum), default=AppointmentStatusEnum.scheduled
    )

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    medical_record = relationship(
        "MedicalRecord", back_populates="appointment", uselist=False
    )
