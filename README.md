# 🏥 Healthcare Appointment Scheduling System

A secure and scalable backend system for managing patients, doctors, and healthcare appointments. This project leverages **FastAPI**, **PostgreSQL**, and **Celery with Redis** for asynchronous processing to deliver a robust solution for real-world healthcare workflows.

---

## 🔧 Features

- **Patient Management**: Register, view, and manage patient profiles with basic details and insurance information.
- **Doctor Management**: Register and manage doctors with specializations and configurable availability schedules.
- **Appointment Scheduling**: Book, list, and cancel appointments with real-time availability checks and conflict prevention.
- **Medical Records**: Add and retrieve patient records linked to appointments with access control.
- **Authentication & Authorization**: Role-based access control using OAuth2 + JWT.
- **Async Email Notifications**: Background task processing using Celery + Redis.

---

## 🧱 Tech Stack

| Layer    | Technology        |
| -------- | ----------------- |
| Backend  | FastAPI (Python)  |
| Database | MySQL             |
| Auth     | OAuth2 + JWT      |
| Queue    | Celery with Redis |
| Docs     | Swagger (OpenAPI) |

---

## 🚀 Getting Started

### ✅ Prerequisites

- Docker & Docker Compose

---

### 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/Ras-Pekt/appointment_scheduling_system.git
cd appointment_scheduling_system
```

2. Create a `.env` file:

```env
# .env
MYSQL_ROOT_PASSWORD=<mysql_root_password>
MYSQL_USER=<app_admin>
MYSQL_PASSWORD=<app_admin_password>
MYSQL_DATABASE=<mysql_db>
ADMIN_EMAIL=<admin_email>
ADMIN_PASSWORD=<admin_password>
EMAIL_ADDRESS=<your_email_address>
EMAIL_PASSWORD=<your_email_password>
SECRET_KEY=<secret_key>
```

**Note:** A default root admin account is created on initialization of the app. This account is required to create other Admin accounts (as only an Admin can create Admin accounts). The login details for this account are:

- **Email:** Specified in `ADMIN_EMAIL`
- **Password:** Specified in `ADMIN_PASSWORD`

3. Run the app:

```bash
docker-compose up --build
```

4. Access Swagger UI:

```
http://0.0.0.0:8000/docs
```

---

## 📚 API Overview

### 🔐 Auth

| Endpoint      | Method | Description             | Access |
| ------------- | ------ | ----------------------- | ------ |
| `/auth/login` | POST   | Obtain JWT access token | Public |

---

### 👤 Users (Admin Only)

| Endpoint             | Method | Description              |
| -------------------- | ------ | ------------------------ |
| `/users/`            | GET    | List all users           |
| `/users/{user_id}`   | GET    | Retrieve a specific user |
| `/users/new-admin`   | POST   | Register a new admin     |
| `/users/new-doctor`  | POST   | Register a new doctor    |
| `/users/new-patient` | POST   | Register a new patient   |
| `/users/{user_id}`   | DELETE | Delete a user by ID      |

---

### 👨‍⚕️ Doctors

| Endpoint                                              | Method | Description                                       | Access      |
| ----------------------------------------------------- | ------ | ------------------------------------------------- | ----------- |
| `/doctors/me`                                         | GET    | Get the logged-in doctor's profile                | Doctor Only |
| `/doctors/all-doctors`                                | GET    | List all doctors (optional specialization filter) | Public      |
| `/doctors/appointments`                               | GET    | Get all appointments for logged-in doctor         | Doctor Only |
| `/doctors/new-availability-slot`                      | POST   | Add new availability slots                        | Doctor Only |
| `/doctors/availability/change-availability/{slot_id}` | PATCH  | Change availability slot status                   | Doctor Only |
| `/doctors/availability/delete-availability/{slot_id}` | DELETE | Delete availability slot                          | Doctor Only |
| `/doctors/new-medical-report/{appointment_id}`        | POST   | Create a new medical record                       | Doctor Only |
| `/doctors/medical-records`                            | GET    | List all medical records created by doctor        | Doctor Only |
| `/doctors/medical-records/{patient_id}`               | GET    | Get records for a specific patient                | Doctor Only |

---

### 🧑‍⚕️ Patients

| Endpoint                                    | Method | Description                                     | Access       |
| ------------------------------------------- | ------ | ----------------------------------------------- | ------------ |
| `/patients/register-new-patient`            | POST   | Self-register as a new patient                  | Public       |
| `/patients/view-all-doctors`                | GET    | View all doctors                                | Patient Only |
| `/patients/doctor/availability/{doctor_id}` | GET    | View availability of a specific doctor          | Patient Only |
| `/patients/create-new-appointment`          | POST   | Create a new appointment                        | Patient Only |
| `/patients/doctor/appointments`             | GET    | View all appointments booked by current patient | Patient Only |
| `/patients/doctor/appointments/{doctor_id}` | GET    | View all appointments by doctor ID              | Patient Only |
| `/patients/medical-records/`                | GET    | View all your medical records                   | Patient Only |
| `/patients/medical-records/{doctor_id}`     | GET    | View medical records from a specific doctor     | Patient Only |

---

### 🕕 Appointments

| Endpoint            | Method | Description                                      | Access       |
| ------------------- | ------ | ------------------------------------------------ | ------------ |
| `/appointments`     | GET    | List all appointments for logged-in doctor       | Doctor Only  |
| `/appointments/new` | POST   | Book a new appointment (with availability check) | Patient Only |

---

### 📄 Medical Records (Bonus)

| Endpoint                                           | Method | Description                 |
| -------------------------------------------------- | ------ | --------------------------- |
| `/medical-records/new-medical-report/{patient_id}` | POST   | Create new medical record   |
| `/medical-records/{patient_id}`                    | GET    | Get patient medical records |

---

## ⚙️ Architecture Overview

- **Modular App Structure**: Organized per domain (`patients/`, `doctors/`, etc.)
- **RBAC System**: Centralized logic in `deps/auth.py`
- **Async Messaging**: Celery queues for non-blocking email tasks
- **MySQL for Production**: Full relational support

---

## 🛡️ Security

- OAuth2 Password Flow with JWT
- Passwords hashed with bcrypt
- Role-based endpoint access
- Sensitive data (e.g., records) scoped by user role

---

## 🧱 Documentation

- 📄 Swagger UI: `http://0.0.0.0:8000/docs`
- 🗜️ Redoc: `http://0.0.0.0:8000/redoc`
- 🗂️ Database schema: [`/docs/schema.png`](docs/schema.png)
- 🖁️ Sequence diagram: [`/docs/sequence.png`](docs/sequence.png)

---

## 🧐 Design Decisions

- Chose **FastAPI** for async support, clean syntax, and OpenAPI docs.
- Modular folder structure for scalability and maintainability.
- Celery used to handle non-blocking async tasks (e.g., email).
- Separated SQLite testing environment for CI/CD speed.
- PostgreSQL in production for advanced indexing and relational features.

---

## 👨‍💼 Author

**Wanjang'i Gituku**  
_Fullstack Developer_  
📧 wanjangi.gituku@gmail.com  
🔗 [Portfolio](https://wanjangi-gituku.github.io/online-portfolio/)

---

## 📃 License

See [LICENSE](https://creativecommons.org/licenses/by-nc/4.0/) details.
