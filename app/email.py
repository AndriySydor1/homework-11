import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv
from typing import List

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування конфігурації для SMTP сервера
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

# Функція для відправлення листа з підтвердженням
async def send_verification_email(email: EmailStr, token: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],  # Список одержувачів
        body=f"Please verify your email by clicking on the following link: http://127.0.0.1:8000/verify-email?token={token}",
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

# Функція для відправлення повідомлення
async def send_email(subject: str, email_to: List[EmailStr], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

# Функція для відправлення листа з скиданням паролю
async def send_reset_password_email(email: EmailStr, token: str, background_tasks: BackgroundTasks):
    reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],  # Список одержувачів
        body=f"To reset your password, click the following link: {reset_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
