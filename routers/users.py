from fastapi import APIRouter, HTTPException, status
from models.patient import Patient
from models.doctor import Doctor
from models.user import User
from routers import Admin_Dependency, DB_Dependency, create_user
from schemas.doctor import DoctorCreate
from schemas.patient import PatientCreate
from schemas.user import AdminOut, UserCreate, UserOut
from tasks.email import send_welcome_email

users_router = APIRouter(
    prefix="/admin",
    tags=["Admins"],
)


@users_router.get(
    "/all-users", response_model=list[UserOut], status_code=status.HTTP_200_OK
)
async def get_all_users(db: DB_Dependency, current_user: Admin_Dependency):
    """
    Retrieve all users from the database.

    Args:
        db (DB_Dependency): The database dependency.

    Returns:
        list: A list of all users.
    """
    all_users = db.query(User).all()
    return all_users


@users_router.get(
    "/user/{user_id}", response_model=AdminOut, status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    user_id: str, db: DB_Dependency, current_user: Admin_Dependency
):
    """
    Retrieve a user by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.
        db (DB_Dependency): The database dependency.

    Returns:
        User: The user object.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@users_router.post("/register-new-admin", status_code=status.HTTP_201_CREATED)
async def register_new_admin(user_data: UserCreate, db: DB_Dependency):
    """
    Register a new admin user.

    Args:
        user_data (UserCreate): The user data to register.
        db (DB_Dependency): The database dependency.

    Returns:
        dict: A dictionary containing a success message.
    """
    if user_data.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User role must be 'admin'",
        )
    create_user(user_data.model_dump(), db)

    send_welcome_email.delay(email=user_data.email, first_name=user_data.first_name)

    return {"message": "Admin registered successfully"}


@users_router.post("/register-new-doctor", status_code=status.HTTP_201_CREATED)
async def register_new_doctor(
    doctor_data: DoctorCreate, db: DB_Dependency, current_user: Admin_Dependency
):
    """
    Register a new doctor user.

    Args:
        doctor_data (DoctorCreate): The doctor data to register.
        db (DB_Dependency): The database dependency.

    Returns:
        dict: A dictionary containing a success message.
    """

    user_data = {
        "email": doctor_data.email,
        "first_name": doctor_data.first_name,
        "last_name": doctor_data.last_name,
        "role": doctor_data.role,
        "hashed_password": doctor_data.hashed_password,
    }

    user_id = create_user(user_data, db)

    new_doctor = Doctor(user_id=user_id, specialization=doctor_data.specialization)

    if doctor_data.role.name != "doctor":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User role must be 'doctor'",
        )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    send_welcome_email.delay(email=doctor_data.email, first_name=doctor_data.first_name)

    return {"message": "Doctor registered successfully"}


@users_router.post("/register-new-patient", status_code=status.HTTP_201_CREATED)
async def register_new_patient(
    patient_data: PatientCreate, db: DB_Dependency, current_user: Admin_Dependency
):
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

    send_welcome_email(email=patient_data.email, first_name=patient_data.first_name)

    return {"message": "patient registered successfully"}


@users_router.delete("/delete-user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, db: DB_Dependency, current_user: Admin_Dependency):
    """
    Delete a user by their ID.

    Args:
        user_id (str): The ID of the user to delete.
        db (DB_Dependency): The database dependency.

    Returns:
        dict: A dictionary containing a success message.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
