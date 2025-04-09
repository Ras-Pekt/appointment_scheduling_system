from typing import Optional
from fastapi import APIRouter, HTTPException, status

from models.availability import Availability
from models.doctor import Doctor
from routers import DB_Dependency
from schemas.availability import AvailabilityCreate
from schemas.doctor import DoctorOut

doctors_router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@doctors_router.get("/all-doctors", response_model=list[DoctorOut])
async def get_all_doctors(db: DB_Dependency, specilization: Optional[str] = None):
    """
    Retrieve all doctors from the database.

    Args:
        db (DB_Dependency): The database dependency.
        specilization (Optional[str], optional): The specilization of the doctor. Defaults to None.

    Returns:
        list: A list of all doctors.
    """
    if specilization is None:
        all_doctors = db.query(Doctor).all()
        if not all_doctors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Doctors found",
            )
        return all_doctors

    all_doctors = db.query(Doctor).filter(Doctor.specialization == specilization).all()
    if not all_doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Doctors with that specilization found",
        )
    return all_doctors


@doctors_router.post("/new-availability-slot")
async def create_new_availability_slot(
    availability_data: AvailabilityCreate, db: DB_Dependency
):
    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.user_id
            == "44b451fd-c2b3-43f8-9920-8c74320279f1"  # replace this with the actual doctor ID
        )
        .first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    new_slot = Availability(
        weekday=availability_data.weekday,
        start_time=availability_data.start_time,
        end_time=availability_data.end_time,
        doctor_id="44b451fd-c2b3-43f8-9920-8c74320279f1",  # replace this with the actual doctor ID
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return {"message": "New availability slot created"}
