from fastapi import FastAPI
from routers.appointments import appointments_router
from routers.patients import patients_router
from routers.doctors import doctors_router
from routers.users import users_router

app = FastAPI()

app.include_router(appointments_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(users_router)
