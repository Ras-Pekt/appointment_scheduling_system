import smtplib
from email.message import EmailMessage
from celery import Celery
from core.config import settings

celery = Celery("email_tasks", broker="redis://redis:6379/0")


def send_email(subject: str, recipient: str, body: str):
    """
    Send an email.

    Args:
        subject (str): The subject of the email.
        recipient (str): The email address of the recipient.
        body (str): The body of the email.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        smtp.send_message(msg)


@celery.task
def send_welcome_email(email: str, first_name: str):
    """
    Send a welcome email to the user.

    Args:
        email (str): The email address of the user.
        first_name (str): The first name of the user.
    """
    subject = "Welcome to Our HealthCare Platform"
    body = f"Hi {first_name},\n\nThank you for registering. We're excited to have you!"
    send_email(subject, email, body)


@celery.task
def notify_appointment_creation(email: str, doctor_name: str, date_time: str):
    """
    Send an email notification to the user when an appointment is created.

    Args:
        email (str): The email address of the user.
        doctor_name (str): The name of the doctor who created the appointment.
        date_time (str): The date and time of the appointment.
    """
    subject = "New Appointment Confirmation"
    body = f"Dear {email},\n\nYour appointment with Dr. {doctor_name} is confirmed for {date_time}."
    send_email(subject, email, body)


@celery.task
def notify_new_medical_record_creation(email: str, doctor_name: str):
    """
    Send an email notification to the user when a new medical record is added.

    Args:
        email (str): The email address of the user.
        doctor_name (str): The name of the doctor who added the medical record.
    """
    subject = "New Medical Record Added"
    body = f"Dear {email},\n\nA new medical record has been added to your profile by Dr. {doctor_name}."
    send_email(subject, email, body)
