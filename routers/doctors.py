from typing import Optional
from fastapi import APIRouter, HTTPException
from starlette import status

from models.appointment import Appointment
from models.availability import Availability
from models.doctor import Doctor
from models.medical_record import MedicalRecord
from routers import DB_Dependency, Doctor_Dependency
from schemas.appointment import AppointmentOut
from schemas.availability import AvailabilityCreate
from schemas.doctor import DoctorOut
from schemas.medical_record import MedicalRecordCreate, MedicalRecordOut
from tasks.email import notify_new_medical_record_creation

doctors_router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@doctors_router.get("/me", response_model=DoctorOut, status_code=status.HTTP_200_OK)
async def view_doctor_profile(db: DB_Dependency, current_doctor: Doctor_Dependency):
    """
    Retrieve the current doctor's profile.

    Args:
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor dependency.

    Returns:
        Doctor: The current doctor's profile.
    """
    current_doctor = db.query(Doctor).filter(Doctor.id == current_doctor.id).first()
    if not current_doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to view this profile",
        )
    return current_doctor


@doctors_router.get(
    "/all-doctors", response_model=list[DoctorOut], status_code=status.HTTP_200_OK
)
async def view_all_doctors(
    db: DB_Dependency,
    current_doctor: Doctor_Dependency,
    specilization: Optional[str] = None,
):
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


@doctors_router.post("/new-availability-slot", status_code=status.HTTP_201_CREATED)
async def create_new_availability_slot(
    availability_data: AvailabilityCreate,
    db: DB_Dependency,
    current_doctor: Doctor_Dependency,
):
    """
    Create a new availability slot for a doctor.

    Args:
        availability_data (AvailabilityCreate): The availability data to create.
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor.

    Returns:
        dict: A dictionary containing a success message.
    """
    doctor = db.query(Doctor).filter(Doctor.user_id == current_doctor.id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    try:
        new_slot = Availability(
            weekday=availability_data.weekday,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time,
            doctor_id=doctor.id,
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create availability slot: {str(e)}",
        )

    return {"message": "New availability slot created"}


@doctors_router.patch(
    "/availability/change-availability/{slot_id}", status_code=status.HTTP_200_OK
)
async def change_availability(
    slot_id: str,
    db: DB_Dependency,
    current_doctor: Doctor_Dependency,
):
    """
    Change the availability status of an availability slot.

    Args:
        slot_id (str): The ID of the availability slot to change.
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor.

    Returns:
        dict: A dictionary containing a success message.
    """
    availability = (
        db.query(Availability)
        .filter(Availability.id == slot_id, Availability.doctor_id == current_doctor.id)
        .first()
    )

    if not availability:
        raise HTTPException(status_code=404, detail="Availability slot not found")

    if availability.doctor_id != current_doctor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to change this availability slot",
        )

    try:
        availability.available = not availability.available
        db.commit()
        db.refresh(availability)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update availability slot: {str(e)}",
        )

    return {"message": "Availability status updated"}


@doctors_router.delete(
    "/availability/delete-availability/{slot_id}", status_code=status.HTTP_200_OK
)
async def delete_availability(
    slot_id: str, db: DB_Dependency, current_doctor: Doctor_Dependency
):
    """
    Delete an availability slot.

    Args:
        slot_id (str): The ID of the availability slot to delete.
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor.

    Returns:
        dict: A dictionary containing a success message.
    """
    availability = (
        db.query(Availability)
        .filter(Availability.id == slot_id, Availability.doctor_id == current_doctor.id)
        .first()
    )

    if not availability:
        raise HTTPException(status_code=404, detail="Availability slot not found")

    db.delete(availability)
    db.commit()

    return {"message": "Availability slot deleted"}


@doctors_router.get(
    "/appointments", response_model=list[AppointmentOut], status_code=status.HTTP_200_OK
)
async def view_all_appointments(db: DB_Dependency, current_doctor: Doctor_Dependency):
    """
    Retrieve the appointments for the current doctor.

    Args:
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor dependency.

    Returns:
        list: A list of appointments for the current doctor.
    """
    appointments = (
        db.query(Appointment).filter(Appointment.doctor_id == current_doctor.id).all()
    )
    return appointments


@doctors_router.post(
    "/new-medical-report/{appointment_id}", status_code=status.HTTP_201_CREATED
)
async def create_new_medical_report(
    appointment_id: str,
    report_data: MedicalRecordCreate,
    db: DB_Dependency,
    current_doctor: Doctor_Dependency,
):
    """
    Create a new medical report for an appointment.

    Args:
        report_data (MedicalRecordCreate): The medical record data to create.
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor.

    Returns:
        dict: A dictionary containing a success message.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.doctor_id != current_doctor.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to add record for this appointment"
        )

    if appointment.medical_record:
        raise HTTPException(
            status_code=400, detail="Medical record already exists for this appointment"
        )

    try:
        new_record = MedicalRecord(
            doctor_id=current_doctor.id,
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
            notes=report_data.notes,
        )

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create medical record: {str(e)}",
        )

    notify_new_medical_record_creation.delay(
        email=appointment.patient.email, doctor_name=current_doctor.name
    )

    return {"message": "New medical report created"}


@doctors_router.get(
    "/medical-records",
    response_model=list[MedicalRecordOut],
    status_code=status.HTTP_200_OK,
)
async def view_all_doctor_medical_records(
    db: DB_Dependency, current_doctor: Doctor_Dependency
):
    """
    Retrieve the medical records for the current doctor.

    Args:
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor dependency.

    Returns:
        list: A list of medical records for the current doctor.
    """
    medical_records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.doctor_id == current_doctor.id)
        .all()
    )
    if not medical_records:
        raise HTTPException(status_code=404, detail="No medical records found")
    return medical_records


@doctors_router.get(
    "/medical-records/{patient_id}",
    response_model=list[MedicalRecordOut],
    status_code=status.HTTP_200_OK,
)
async def view_all_medical_records_by_patient_id(
    patient_id: str, db: DB_Dependency, current_doctor: Doctor_Dependency
):
    """
    Retrieve the medical records for a patient.

    Args:
        patient_id (str): The ID of the patient.
        db (DB_Dependency): The database dependency.
        current_doctor (Doctor_Dependency): The current doctor.

    Returns:
        list: A list of medical records for the patient.
    """
    medical_records = (
        db.query(MedicalRecord)
        .filter(
            MedicalRecord.doctor_id == current_doctor.id,
            MedicalRecord.patient_id == patient_id,
        )
        .all()
    )
    if not medical_records:
        raise HTTPException(status_code=404, detail="No medical records found")
    return medical_records
