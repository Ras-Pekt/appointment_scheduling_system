from fastapi import APIRouter
from models.patient import Patient
from routers import DB_Dependency

patients_router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@patients_router.get("/")
async def get_patients():
    print("Get all patients")
    return {"message": "Get all patients"}


@patients_router.post("/new-patient")
async def register_new_patient(patient_data, db: DB_Dependency):
    new_patient = Patient(**patient_data.model_dump())
    db.add(new_patient)
    db.commit()
    return {"message": "Patient registered successfully", "new_patient": new_patient}
