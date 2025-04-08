from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from deps.utils import generate_uuid


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String(length=36), ForeignKey("users.id", ondelete="CASCADE"))
    insurance_provider = Column(String(length=255), nullable=True)
    insurance_number = Column(String(length=255), nullable=True)

    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
