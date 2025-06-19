from celery import Celery
from celery_tasks.celery_config import CeleryConfig

app = Celery("book_reviews")
app.config_from_object(CeleryConfig)
app.autodiscover_tasks(["backend.celery_app.tasks"])
