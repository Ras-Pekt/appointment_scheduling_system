from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from deps.utils import generate_uuid


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String(length=36), ForeignKey("users.id", ondelete="CASCADE"))
    specialization = Column(String(length=255), nullable=False)

    user = relationship("User", back_populates="doctor_profile")
    availability = relationship(
        "Availability", back_populates="doctor", cascade="all, delete"
    )
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")
