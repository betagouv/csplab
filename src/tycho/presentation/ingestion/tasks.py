import asyncio

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
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


@db_periodic_task(crontab(day="1", hour="6"))
def clean_metiers():
    clean_documents(DocumentType.METIERS)


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


@db_periodic_task(crontab(day="1", hour="5"))
def load_corps():
    kwargs = {"document_type": DocumentType.CORPS}
    load_documents(kwargs, usecase_name="load_documents_usecase")


@db_periodic_task(crontab(day="1", hour="5"))
def load_metiers():
    kwargs = {"document_type": DocumentType.METIERS}
    load_documents(kwargs, usecase_name="load_documents_usecase")


@db_periodic_task(crontab(hour="5-21", minute="0"))
def load_offers(reload=False, batch_size=100, max_pages=0):
    kwargs = {
        "document_type": DocumentType.OFFERS,
        "reload": reload,
        "batch_size": batch_size,
        "max_pages": max_pages,
    }
    load_documents(kwargs, usecase_name="load_offers_usecase")


@db_task()
def load_documents(kwargs, usecase_name):
    container = create_ingestion_container()
    logger = container.logger_service()
    usecase = getattr(container, usecase_name)()
    input_data = LoadDocumentsInput(
        operation_type=LoadOperationType.FETCH_FROM_API, kwargs=kwargs
    )
    try:
        result = asyncio.run(usecase.execute(input_data))
        logger.info(
            "✅ Load completed: %d created, %d updated",
            result["created"],
            result["updated"],
        )
        if result["errors"]:
            logger.warning("⚠️ %d errors occurred", len(result["errors"]))

    except Exception as e:
        raise TaskError(
            message=f"Failed to load documents type {kwargs['document_type']}",
            details={"error": str(e)},
        ) from e
