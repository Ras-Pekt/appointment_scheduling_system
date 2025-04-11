from fastapi import FastAPI
from core.security import hash_password
from models.user import User
from routers.patients import patients_router
from routers.doctors import doctors_router
from routers.users import users_router
from routers.auth import auth_router
from core.database import Base, engine, SessionLocal
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(users_router)
app.include_router(auth_router)


SUPER_ADMIN_EMAIL = getenv("ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

print("SUPER_ADMIN_EMAIL: ", SUPER_ADMIN_EMAIL)
print("SUPER_ADMIN_PASSWORD: ", SUPER_ADMIN_PASSWORD)

if not SUPER_ADMIN_EMAIL or not SUPER_ADMIN_PASSWORD:
    raise ValueError("ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set")

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

super_admin = User(
    email=SUPER_ADMIN_EMAIL,
    first_name="Super",
    last_name="Admin",
    hashed_password=hash_password(SUPER_ADMIN_PASSWORD),
    role="admin",
)

db.add(super_admin)
db.flush()
db.commit()
db.close()
