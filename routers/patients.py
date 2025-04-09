from fastapi import APIRouter, HTTPException, status
from models.patient import Patient
from routers import DB_Dependency, create_user
from schemas.patient import PatientCreate

patients_router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@patients_router.post("/new-patient")
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

    return {"message": "patient registered successfully", "new_patient": new_patient}
