import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PayloadSchemaType, VectorParams

from config.app_config import AppConfig
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository


def create_collection(client: QdrantClient, collection_name: str):
    # Créer la collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )

    # Créer les index comme dans le script de setup
    indexes = [
        "document_type",
        "category",
        "verse",
        "localisation.region",
        "localisation.country",
        "localisation.department",
    ]

    for field_name in indexes:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=PayloadSchemaType.KEYWORD,
        )


def create_shared_qdrant_repository():
    app_config = AppConfig.from_django_settings()
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    collection_name = f"fonction_publique_test_{worker_id}"
    client = QdrantClient(url=app_config.qdrant.url)

    try:
        client.delete_collection(collection_name=collection_name)
    except Exception:
        logger_service = LoggerService()
        logger_service.warning(
            f"Collection {collection_name} does not exist, skipping deletion."
        )
        pass

    create_collection(client, collection_name)

    logger_service = LoggerService()
    qdrant_repo = QdrantRepository(app_config.qdrant, logger_service)
    qdrant_repo.collection_name = collection_name
    return qdrant_repo
