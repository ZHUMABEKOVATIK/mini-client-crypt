from celery import Celery
from datetime import timedelta
from src.core.config import settings

celery_app = Celery(
    "deribit_tracker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["src.tasks.fetch_prices"],
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "tasks.fetch_prices",
        "schedule": timedelta(seconds=60),
    },
}

celery_app.conf.timezone = "UTC"