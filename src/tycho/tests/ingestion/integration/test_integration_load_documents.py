from unittest.mock import patch

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.ingestion.postgres_document_repository import (
    PostgresDocumentRepository,
)
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.factories.ingres_corps_factories import IngresCorpsApiResponseFactory
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

fake = Faker()


class TestIntegrationCorpsLoadDocumentsUseCase:
    @pytest.fixture(name="documents_integration_usecase")
    def documents_integration_usecase_fixture(self, test_app_config):
        container = IngestionContainer()
        logger_service = LoggerService()

        # Configuration de base
        container.logger_service.override(logger_service)
        container.app_config.override(test_app_config)
        container.shared_container.app_config.override(test_app_config)

        # Mock embedding generator
        embedding_fixtures = load_fixture("embedding_fixtures.json")
        embedding_generator = MockEmbeddingGenerator(embedding_fixtures)
        container.shared_container.embedding_generator.override(embedding_generator)

        # Repositories Postgres (vrais pour l'intégration)
        postgres_document_repo = PostgresDocumentRepository()
        container.document_repository.override(postgres_document_repo)

        postgres_corps_repo = PostgresCorpsRepository(logger_service)
        container.shared_container.corps_repository.override(postgres_corps_repo)

        postgres_concours_repo = PostgresConcoursRepository(logger_service)
        container.shared_container.concours_repository.override(postgres_concours_repo)

        postgres_offers_repo = PostgresOffersRepository(logger_service)
        container.shared_container.offers_repository.override(postgres_offers_repo)

        # InMemoryVectorRepository pour éviter Qdrant
        in_memory_vector_repo = InMemoryVectorRepository(logger_service)
        container.shared_container.vector_repository.override(in_memory_vector_repo)

        return container.load_documents_usecase()

    async def test_execute_returns_zero_when_no_documents(
        self, db, documents_integration_usecase, test_app_config, httpx_mock
    ):
        # Mock OAuth token endpoint
        httpx_mock.add_response(
            method="POST",
            url=f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status_code=200,
        )

        # Mock INGRES API endpoint with empty response
        httpx_mock.add_response(
            method="GET",
            url=f"{test_app_config.ingres_base_url}/CORPS",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": []},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = await documents_integration_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    async def test_execute_returns_correct_count_with_documents(
        self, db, documents_integration_usecase, test_app_config, httpx_mock
    ):
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        httpx_mock.add_response(
            method="POST",
            url=f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status_code=200,
        )

        # Mock INGRES API endpoint
        httpx_mock.add_response(
            method="GET",
            url=f"{test_app_config.ingres_base_url}/CORPS",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": api_data},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = await documents_integration_usecase.execute(input_data)
        assert result["created"] == len(api_data)
        assert result["updated"] == 0

        # Verify documents are persisted in database
        @sync_to_async
        def get_saved_documents_count():
            return RawDocument.objects.filter(
                document_type=DocumentType.CORPS.value
            ).count()

        saved_count = await get_saved_documents_count()
        assert saved_count == len(api_data)


@pytest.fixture(name="api_client")
def api_client_fixture():
    return APIClient()


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


class TestHueyHealthView:
    url = reverse("ingestion:health_huey")

    def test_success_response(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_access(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_redis_unavailable(self, authenticated_client):
        with patch("huey.contrib.djhuey.HUEY.storage.conn.ping") as mocked_ping:
            mocked_ping.side_effect = Exception("Redis connection refused")
            response = authenticated_client.get(self.url)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data == {"status": "Huey health check failed"}


@pytest.fixture(name="valid_csv_content")
def valid_csv_content_fixture():
    return (
        "N° NOR;Ministère;Catégorie;Corps;"
        "Grade;Année de référence;Nb postes total\n"
        "INTB2400001C;Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
        "INTB2400002C;Ministère de l'Intérieur;B;Secrétaire;Secrétaire;2024;5\n"
    )


@pytest.fixture(name="invalid_csv_content")
def invalid_csv_content_fixture():
    return (
        "N° NOR;Ministère;Catégorie;Corps;Grade;"
        "Année de référence;Nb postes total\n"
        ";Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
        "INTB2400002C;;B;Secrétaire;Secrétaire;2024;5\n"
    )


def make_csv_file(content, filename="test.csv"):
    return SimpleUploadedFile(
        filename, content.encode("utf-8"), content_type="text/csv"
    )


class TestConcoursUploadView:
    url = reverse("ingestion:concours_upload")

    def test_unauthenticated_access(self, api_client, valid_csv_content):
        response = api_client.post(
            self.url, {"file": make_csv_file(valid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_no_file_provided(self, authenticated_client):
        response = authenticated_client.post(self.url, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No file provided"

    def test_invalid_file_format(self, authenticated_client):
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )
        response = authenticated_client.post(
            self.url, {"file": txt_file}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "File must be a CSV"

    def test_validation_errors(self, authenticated_client, invalid_csv_content):
        response = authenticated_client.post(
            self.url, {"file": make_csv_file(invalid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No valid rows found"
        assert "validation_errors" in response.data
        assert len(response.data["validation_errors"]) == 2  # noqa

    def test_success_response(self, db, authenticated_client, valid_csv_content):
        response = authenticated_client.post(
            self.url, {"file": make_csv_file(valid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "success"
        assert response.data["total_rows"] == 2  # noqa
        assert response.data["valid_rows"] == 2  # noqa
        assert response.data["invalid_rows"] == 0
        assert (
            "Successfully processed 2 valid concours records"
            in response.data["message"]
        )
