from celery import Celery
from celery.signals import setup_logging

from api.config import settings
from infrastructure.observability.log_config import configure_logging


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


@setup_logging.connect
def _configure_worker_logging(**kwargs: object) -> None:
    configure_logging(settings.log_level)
