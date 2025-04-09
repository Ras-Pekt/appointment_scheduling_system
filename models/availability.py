from sqlalchemy import Column, String, ForeignKey, Time, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from core.enums import WeekdayEnum
from deps.utils import generate_uuid


class Availability(Base):
    __tablename__ = "availability"

    id = Column(String(length=36), primary_key=True, index=True, default=generate_uuid)
    doctor_id = Column(String(length=36), ForeignKey("doctors.id", ondelete="CASCADE"))
    weekday = Column(Enum(WeekdayEnum), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("Doctor", back_populates="availability")
