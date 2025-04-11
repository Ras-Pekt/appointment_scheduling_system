from fastapi import FastAPI
from routers.patients import patients_router
from routers.doctors import doctors_router
from routers.users import users_router
from core.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(users_router)
