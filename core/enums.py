from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class AppointmentStatusEnum(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class WeekdayEnum(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
