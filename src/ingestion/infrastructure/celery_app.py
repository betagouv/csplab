from celery import Celery

from api.config import settings


def create_celery_app() -> Celery:
    app = Celery("ingestion")
    app.conf.update(
        broker_url=settings.redis_url,
        result_backend=None,
        task_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        include=["application.tasks.process_webhook"],
    )
    return app


celery_app = create_celery_app()
