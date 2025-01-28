import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

from backend.config import Settings


def send_email(mail_body: str, mail_theme: str, receiver_email: str):
    sender_login = Settings.LOGIN
    password = Settings.PASSWORD

    print(f"Sender Login: {sender_login}")
    print(f"Password: {password}")
    print(f"Receiver Email: {receiver_email}")

    if sender_login is None or password is None or receiver_email is None:
        return "Error: One of the required fields is None"

    subject = mail_theme
    message = f"Subject: {subject}\n\n{mail_body}".encode('utf-8')

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    try:
        server.login(sender_login, password)
        server.sendmail(sender_login, receiver_email, message)
        return "Message sent"

    except Exception as e:
        print(f"Error: {e}")
        return str(e)


send_email(mail_body='Проверка тело', mail_theme='Проверка тема', receiver_email='elizavetalenn@mail.ru')
