from fastapi import APIRouter, HTTPException
from starlette import status
from core.enums import WeekdayEnum
from models.appointment import Appointment
from models.availability import Availability
from models.doctor import Doctor
from models.medical_record import MedicalRecord
from models.patient import Patient
from routers import DB_Dependency, Patient_Dependency, create_user
from schemas.appointment import AppointmentCreate, AppointmentOut
from schemas.availability import AvailabilitySlotResponse
from schemas.doctor import DoctorOut
from schemas.medical_record import MedicalRecordOut
from schemas.patient import PatientCreate
from tasks.email import notify_appointment_creation, send_welcome_email

patients_router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@patients_router.post("/register-new-patient", status_code=status.HTTP_201_CREATED)
async def register_new_patient(patient_data: PatientCreate, db: DB_Dependency):
    """
    Register a new patient user.

    Args:
        patient_data (PatientCreate): The patient data to register.
        db (DB_Dependency): The database dependency.

    Returns:
        dict: A dictionary containing a success message.
    """
    user_data = {
        "email": patient_data.email,
        "first_name": patient_data.first_name,
        "last_name": patient_data.last_name,
        "role": patient_data.role,
        "hashed_password": patient_data.hashed_password,
    }

    user_id = create_user(user_data, db)

    try:
        new_patient = Patient(
            user_id=user_id,
            insurance_provider=patient_data.insurance_provider,
            insurance_number=patient_data.insurance_number,
        )

        if patient_data.role.name != "patient":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User role must be 'patient'",
            )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    send_welcome_email.delay(
        email=patient_data.email, first_name=patient_data.first_name
    )

    return {"message": "patient registered successfully"}


@patients_router.post("/create-new-appointment", status_code=status.HTTP_201_CREATED)
async def create_new_appointment(
    appointment_data: AppointmentCreate,
    db: DB_Dependency,
    current_patient: Patient_Dependency,
):
    """
    Create a new appointment for a patient.

    Args:
        appointment_data (AppointmentCreate): The appointment data to create.
        db (DB_Dependency): The database dependency.
        current_patient (Patient_Dependency): The current patient dependency.

    Returns:
        dict: A dictionary containing a success message.
    """
    patient = db.query(Patient).filter(Patient.user_id == current_patient.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    appointment_weekday = WeekdayEnum(
        appointment_data.scheduled_start.strftime("%A").upper()
    )

    if appointment_data.scheduled_start >= appointment_data.scheduled_end:
        raise HTTPException(status_code=400, detail="Invalid time range")

    # Check if a valid availability slot exists
    slot = (
        db.query(Availability)
        .filter(
            Availability.doctor_id == appointment_data.doctor_id,
            Availability.weekday == appointment_weekday,
            Availability.start_time <= appointment_data.scheduled_start.time(),
            Availability.end_time >= appointment_data.scheduled_end.time(),
            Availability.available == True,
        )
        .first()
    )

    if not slot:
        raise HTTPException(
            status_code=400,
            detail="Doctor is not available at the selected time",
        )

    # Check for overlapping appointments
    conflict = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment_data.doctor_id,
            Appointment.scheduled_start < appointment_data.scheduled_end,
            Appointment.scheduled_end > appointment_data.scheduled_start,
        )
        .first()
    )

    if conflict:
        raise HTTPException(
            status_code=409,
            detail="This appointment overlaps with an existing one",
        )

    new_appointment = Appointment(
        doctor_id=appointment_data.doctor_id,
        patient_id=patient.id,
        scheduled_start=appointment_data.scheduled_start,
        scheduled_end=appointment_data.scheduled_end,
        status=appointment_data.status,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    notify_appointment_creation.delay(
        email=patient.email,
        doctor_name=new_appointment.doctor.name,
        date_time=new_appointment.scheduled_start,
    )

    return {"message": "New appointment created"}


@patients_router.get(
    "/view-all-doctors", response_model=list[DoctorOut], status_code=status.HTTP_200_OK
)
async def view_all_doctors(db: DB_Dependency, current_patient: Patient_Dependency):
    """
    Retrieve all doctors from the database.

    Args:
        db (DB_Dependency): The database dependency.

    Returns:
        list: A list of all doctors.
    """
    all_doctors = db.query(Doctor).all()
    if not all_doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Doctors found",
        )
    return all_doctors


@patients_router.get(
    "/doctor/availability/{doctor_id}",
    response_model=list[AvailabilitySlotResponse],
    status_code=status.HTTP_200_OK,
)
async def view_doctor_availability_by_doctor_id(
    doctor_id: str, db: DB_Dependency, current_patient: Patient_Dependency
):
    """
    Retrieve the availability slots for a doctor.

    Args:
        doctor_id (str): The ID of the doctor.
        db (DB_Dependency): The database dependency.

    Returns:
        list: A list of availability slots for the doctor.
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    availability_slots = (
        db.query(Availability).filter(Availability.doctor_id == doctor_id).all()
    )

    if not availability_slots:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No availabile slots found for this doctor",
        )

    # Check for booked appointments within the availability slots
    availability_responses = []
    for slot in availability_slots:
        # Check if there's any existing appointment that overlaps with this availability slot
        booked_appointments = (
            db.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id,
                Appointment.scheduled_start < slot.end_time,
                Appointment.scheduled_end > slot.start_time,
            )
            .all()
        )

        # If there are booked appointments, mark the slot as unavailable
        is_available = len(booked_appointments) == 0

        availability_responses.append(
            AvailabilitySlotResponse(
                weekday=slot.weekday.name,
                start_time=slot.start_time,
                end_time=slot.end_time,
                available=is_available,
            )
        )

    # Construct the DoctorResponse object
    doctor_response = DoctorOut(
        id=doctor.id,
        specialization=doctor.specialization,
        availability=availability_responses,
        email=doctor.user.email,
        first_name=doctor.user.first_name,
        last_name=doctor.user.last_name,
    )

    return doctor_response


@patients_router.get(
    "/doctor/appointments",
    response_model=list[AppointmentOut],
    status_code=status.HTTP_200_OK,
)
async def view_my_appointments(current_user: Patient_Dependency, db: DB_Dependency):
    """
    Retrieve the appointments for the current patient.

    Args:
        current_user (Patient_Dependency): The current patient dependency.
        db (DB_Dependency): The database dependency.

    Returns:
        list: A list of appointments for the current patient.
    """
    appointments = (
        db.query(Appointment).filter(Appointment.patient_id == current_user.id).all()
    )
    return appointments


@patients_router.get(
    "/doctor/appointments/{doctor_id}",
    response_model=list[AppointmentOut],
    status_code=status.HTTP_200_OK,
)
async def view_all_appointments_by_doctor_id(
    doctor_id: str, db: DB_Dependency, current_user: Patient_Dependency
):
    """
    Retrieve the appointments for a specific doctor.

    Args:
        doctor_id (str): The ID of the doctor.
        db (DB_Dependency): The database dependency.

    Returns:
        list: A list of appointments for the doctor.
    """
    appointments = (
        db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
    )
    if not appointments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No appointments found for this doctor",
        )
    return appointments


@patients_router.get(
    "/medical-records/",
    response_model=list[MedicalRecordOut],
    status_code=status.HTTP_200_OK,
)
async def view_all_medical_records(db: DB_Dependency, current_user: Patient_Dependency):
    """
    Retrieve the medical records for the current patient.

    Args:
        db (DB_Dependency): The database dependency.
        current_user (Patient_Dependency): The current patient dependency.

    Returns:
        list: A list of medical records for the current patient.
    """
    medical_records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == current_user.id)
        .all()
    )
    if not medical_records:
        raise HTTPException(status_code=404, detail="No medical records found")
    return medical_records


@patients_router.get(
    "/medical-records/{doctor_id}",
    response_model=list[MedicalRecordOut],
    status_code=status.HTTP_200_OK,
)
async def view_all_medical_records_by_doctor_id(
    doctor_id: str, db: DB_Dependency, current_user: Patient_Dependency
):
    """
    Retrieve the medical records from a specific doctor.

    Args:
        doctor_id (str): The ID of the doctor.
        db (DB_Dependency): The database dependency.
        current_user (Patient_Dependency): The current patient dependency.

    Returns:
        list: A list of medical records from a specific doctor.
    """
    medical_records = (
        db.query(MedicalRecord)
        .filter(
            MedicalRecord.doctor_id == doctor_id,
            MedicalRecord.patient_id == current_user.id,
        )
        .all()
    )
    if not medical_records:
        raise HTTPException(status_code=404, detail="No medical records found")
    return medical_records
