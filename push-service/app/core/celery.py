from celery import Celery
from app.core.config import settings
import os

# Configuration du broker RabbitMQ
broker_url = os.getenv("CELERY_BROKER_URL", f"amqp://guest:guest@{settings.RABBITMQ_URL}:{settings.RABBITMQ_PORT}/")
backend_url = os.getenv("CELERY_RESULT_BACKEND", settings.REDIS_URL)

celery_app = Celery(
    "push_service",
    broker=broker_url,
    backend=backend_url
)

# Configuration Celery (nombre de réessais, etc.)
celery_app.conf.update(
    result_expires=3600,  # Résultats expirent après 1 heure
    task_serializer='json',
    accept_content=['json'],  # Tâches acceptées au format JSON
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_annotations={
        '*': {'rate_limit': '10/s'}
    },
)
