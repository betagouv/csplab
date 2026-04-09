from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from infrastructure.exceptions.exceptions import TaskError


@db_periodic_task(crontab(day="1", hour="7"))
def vectorize_corps():
    vectorize_documents(DocumentType.CORPS)


@db_periodic_task(crontab(hour="7"))
def vectorize_concours():
    vectorize_documents(DocumentType.CONCOURS)


@db_periodic_task(crontab(minute="*/10"))
def vectorize_offers():
    vectorize_documents(DocumentType.OFFERS)


@db_task()
def vectorize_documents(document_type: DocumentType):
    container = create_ingestion_container()
    logger = container.logger_service()
    usecase = container.vectorize_documents_usecase()

    try:
        result = usecase.execute(document_type)
        logger.info(
            "✅ Vectorization completed: %d/%d documents of type %s vectorized",
            result["vectorized"],
            result["processed"],
            document_type,
        )

        if result["errors"] > 0:
            logger.warning("⚠️ %d errors occurred", result["errors"])

        if result.get("error_details"):
            for error in result["error_details"]:
                logger.warning(
                    "%s - %s: %s",
                    error["source_type"],
                    error["source_id"],
                    error["error"],
                )
    except Exception as e:
        raise TaskError(
            message=f"Failed to vectorize documents {document_type}",
            details={"error": str(e)},
        ) from e


@db_periodic_task(crontab(day="1", hour="6"))
def clean_corps():
    clean_documents(DocumentType.CORPS)


@db_periodic_task(crontab(hour="6"))
def clean_concours():
    clean_documents(DocumentType.CONCOURS)


@db_periodic_task(crontab(minute="*/10"))
def clean_offers():
    clean_documents(DocumentType.OFFERS)


@db_task()
def clean_documents(document_type: DocumentType):
    container = create_ingestion_container()
    logger = container.logger_service()
    usecase = container.clean_documents_usecase()

    try:
        result = usecase.execute(document_type)
        logger.info(
            "✅ Clean completed: %d/%d documents of type %s cleaned",
            result["cleaned"],
            result["processed"],
            document_type,
        )

        if result["errors"] > 0:
            logger.warning("⚠️ %d errors occurred", result["errors"])

        if result.get("error_details"):
            for error in result["error_details"]:
                logger.warning(
                    "Entity %s: %s",
                    error["entity_id"],
                    error["error"],
                )
    except Exception as e:
        raise TaskError(
            message=f"Failed to clean documents {document_type}",
            details={"error": str(e)},
        ) from e
