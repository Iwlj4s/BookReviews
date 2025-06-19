import asyncio

from celery.celery_app import app
from email.send_email import send_email


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, mail_body: str, mail_theme: str, receiver_email: str):
    try:
        # Создаем новую event loop для асинхронного выполнения
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            send_email(mail_body, mail_theme, receiver_email))
        loop.close()
        return result
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")
        raise self.retry(exc=e)

