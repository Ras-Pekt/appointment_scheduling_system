from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from core.enums import RoleEnum
from deps.utils import generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    hashed_password = Column(String(length=255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
