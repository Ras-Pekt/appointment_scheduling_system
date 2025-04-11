# 🏥 Healthcare Appointment Scheduling System

A secure and scalable backend system for managing patients, doctors, and healthcare appointments. This project leverages **FastAPI**, **PostgreSQL**, and **Celery with Redis** for asynchronous processing to deliver a robust solution for real-world healthcare workflows.

---

## 🔧 Features

- **Patient Management**: Register, view, and manage patient profiles with basic details and insurance information.
- **Doctor Management**: Register and manage doctors with specializations and configurable availability schedules.
- **Appointment Scheduling**: Book, list, and cancel appointments with real-time availability checks and conflict prevention.
- **Medical Records (Bonus)**: Add and retrieve patient records linked to appointments with access control.
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

| Endpoint      | Method | Description      |
| ------------- | ------ | ---------------- |
| `/auth/login` | POST   | Obtain JWT token |

---

### 🧝 Patients

| Endpoint                 | Method | Description          |
| ------------------------ | ------ | -------------------- |
| `/patients/new-patient`  | POST   | Register new patient |
| `/patients/{patient_id}` | GET    | Get patient profile  |
| `/patients`              | GET    | List all patients    |

---

### 👨‍⚕️ Doctors

| Endpoint               | Method | Description             |
| ---------------------- | ------ | ----------------------- |
| `/doctors/new-doctor`  | POST   | Register new doctor     |
| `/doctors/{doctor_id}` | GET    | Get doctor profile      |
| `/doctors`             | GET    | List all doctors        |
| `/availability/`       | POST   | Set doctor availability |

---

### 📅 Appointments

| Endpoint             | Method | Description                    |
| -------------------- | ------ | ------------------------------ |
| `/appointments`      | POST   | Book a new appointment         |
| `/appointments/{id}` | GET    | Get details of one appointment |
| `/appointments`      | GET    | List all appointments          |
| `/appointments/{id}` | DELETE | Cancel an appointment          |

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
- **SQLite for Testing**: Lightweight test DB in CI
- **PostgreSQL for Production**: Full relational support

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

**[Your Full Name]**  
_Junior Fullstack Developer_  
📧 your.email@example.com  
🔗 [GitHub Profile](https://github.com/your-username)

---

## 📃 License

MIT License - See `LICENSE` file for details.
