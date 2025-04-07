from fastapi import FastAPI
from routers.appointments import appointments_router
from routers.patients import patients_router
from routers.doctors import doctors_router

app = FastAPI()

app.include_router(appointments_router)
app.include_router(patients_router)
app.include_router(doctors_router)

# uvicorn main:app --reload --host 0.0.0.0 --port 8000
