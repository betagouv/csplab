import os

import pytest
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connections
from faker import Faker
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PayloadSchemaType, VectorParams
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from config.app_config import AppConfig
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.qdrant_repository import QdrantRepository

fake = Faker()


@pytest.fixture(autouse=True)
async def close_worker_thread_connections():
    yield
    # async ORM calls (via sync_to_async) open a DB connection in a worker thread.
    # close_all() runs in that same thread via sync_to_async, closing the connection
    # before the test database is dropped at session teardown.
    await sync_to_async(connections.close_all)()


@pytest.fixture(name="api_client")
def api_client_fixture():
    return APIClient()


@pytest.fixture(name="user_credentials")
def user_credentials_fixture():
    return {
        "username": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }


@pytest.fixture(name="test_user")
def test_user_fixture(db, user_credentials):
    return User.objects.create_user(**user_credentials)


@pytest.fixture(name="user")
def user_fixture(db):
    return User.objects.create_user(
        username=fake.name(), email=fake.email(), password=fake.password()
    )


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(api_client, user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


def create_collection(client: QdrantClient, collection_name: str):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.EMBEDDING_DIMENSION, distance=Distance.COSINE
        ),
    )

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
