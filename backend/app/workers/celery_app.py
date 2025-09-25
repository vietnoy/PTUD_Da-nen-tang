"""Celery application instance used for background tasks."""
from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "di_cho_tien_loi",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.beat_schedule = {}
celery_app.conf.timezone = "UTC"
