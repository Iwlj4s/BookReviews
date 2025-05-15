import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

load_dotenv()

from backend.config import Settings


async def send_email(mail_body: str, mail_theme: str, receiver_email: str):
    sender_login = Settings.LOGIN
    password = Settings.PASSWORD

    if sender_login is None or password is None or receiver_email is None:
        return "Error: One of the required fields is None"

    # Создаем MIME-сообщение
    msg = MIMEMultipart()
    msg['From'] = sender_login
    msg['To'] = receiver_email
    msg['Subject'] = mail_theme

    # Добавляем HTML-часть
    msg.attach(MIMEText(mail_body, 'html'))

    with smtplib.SMTP("smtp.mail.ru", 587) as server:
        server.starttls()
        server.login(sender_login, password)
        server.send_message(msg)  # Используем send_message вместо sendmail

    return "Message sent"
