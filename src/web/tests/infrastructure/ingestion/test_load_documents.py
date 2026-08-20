import pytest
from asgiref.sync import sync_to_async

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from config.app_config import AppConfig
from domain.ingestion.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.factories.ingestion.ingres_corps_factories import (
    IngresCorpsApiResponseFactory,
)
from infrastructure.gateways.shared.logger import LoggerService

PORT = 6333


@pytest.fixture
def documents_ingestion_container():
    container = IngestionContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(documents_ingestion_container):
    return documents_ingestion_container.app_config()


@pytest.fixture
def load_documents_usecase(documents_ingestion_container):
    return documents_ingestion_container.load_documents_usecase()


class TestIntegrationCorpsLoadDocumentsUseCase:
    async def test_execute_returns_zero_when_no_documents(
        self, db, load_documents_usecase, test_app_config, httpx_mock
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
        result = await load_documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    async def test_execute_returns_correct_count_with_documents(
        self, db, load_documents_usecase, test_app_config, httpx_mock
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
        result = await load_documents_usecase.execute(input_data)
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
