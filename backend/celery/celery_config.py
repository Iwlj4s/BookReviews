from backend.config import Settings


class CeleryConfig:
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "Europe/Moscow"
    enable_utc = True
    broker_connection_retry_on_startup = True

    worker_pool = "solo"  # Add this for Windows
    worker_concurrency = 1  # Add this for Windows

    # Для отправки email'ов
    email_login = Settings.LOGIN
    email_password = Settings.PASSWORD
