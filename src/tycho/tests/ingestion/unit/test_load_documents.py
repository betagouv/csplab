import copy
from datetime import datetime, timezone

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from config.app_config import AppConfig
from domain.entities.document import Document, DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.ingres_corps_factories import (
    IngresCorpsApiResponseFactory,
)
from tests.factories.ingres_metiers_factories import (
    IngresMetiersApiResponseFactory,
)
from tests.utils.in_memory_concours_repository import InMemoryConcoursRepository
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_document_repository import InMemoryDocumentRepository
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository


@pytest.fixture(name="corps_document")
def corps_document_fixture():
    return Document(
        external_id="test_corps_doc",
        raw_data={"name": "Test Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture(name="corps_documents")
def corps_documents_fixture():
    return [
        Document(
            external_id="corps_1",
            raw_data={"name": "Corps 1", "description": "First corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
        ),
        Document(
            external_id="corps_2",
            raw_data={"name": "Corps 2", "description": "Second corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
        ),
    ]


@pytest.fixture(name="concours_documents")
def concours_documents_fixture():
    return [
        Document(
            external_id="exam_1",
            raw_data={"name": "Exam 1"},
            type=DocumentType.CONCOURS,
            created_at=datetime.now(timezone.utc),
        ),
    ]


@pytest.fixture(name="raw_concours_documents")
def raw_concours_documents_fixture(concours_documents):
    return [doc.raw_data for doc in concours_documents]


def create_test_documents(
    documents_ingestion_container,
    raw_data_list,
    doc_type=DocumentType.CORPS,
):
    documents_repository = documents_ingestion_container.document_repository()

    documents = [
        Document(
            external_id=f"test_doc_{i}",
            raw_data={"test": "data", "index": i},
            type=doc_type,
            created_at=datetime.now(timezone.utc),
        )
        for i, _raw_data in enumerate(raw_data_list)
    ]

    documents_repository.upsert_batch(documents, doc_type.value)
    return documents


@pytest.fixture
def documents_ingestion_container():
    container = IngestionContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    in_memory_document_repo = InMemoryDocumentRepository()
    container.document_repository.override(in_memory_document_repo)

    in_memory_corps_repo = InMemoryCorpsRepository()
    shared_container.corps_repository.override(in_memory_corps_repo)

    in_memory_concours_repo = InMemoryConcoursRepository()
    shared_container.concours_repository.override(in_memory_concours_repo)

    in_memory_offers_repo = InMemoryOffersRepository()
    shared_container.offers_repository.override(in_memory_offers_repo)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(documents_ingestion_container):
    return documents_ingestion_container.app_config()


@pytest.fixture
def documents_usecase(documents_ingestion_container):
    return documents_ingestion_container.load_documents_usecase()


class TestCorpsDocumentsUsecase:
    async def test_execute_returns_zero_when_no_documents(
        self, documents_usecase, test_app_config, httpx_mock
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
        result = await documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    async def test_execute_creates_new_documents_when_none_exist(
        self,
        documents_usecase,
        test_app_config,
        httpx_mock,
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
        result = await documents_usecase.execute(input_data)

        assert result["created"] == len(api_data)
        assert result["updated"] == 0


class TestMetiersDocumentsUsecase:
    async def test_execute_returns_zero_when_no_documents(
        self, documents_usecase, test_app_config, httpx_mock
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
            url=f"{test_app_config.ingres_base_url}/RMFP_EMPL_REF",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": []},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.METIERS},
        )
        result = await documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    async def test_execute_creates_new_documents_when_none_exist(
        self,
        documents_usecase,
        test_app_config,
        httpx_mock,
    ):
        api_response = IngresMetiersApiResponseFactory.build()
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
            url=f"{test_app_config.ingres_base_url}/RMFP_EMPL_REF",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": api_data},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.METIERS},
        )
        result = await documents_usecase.execute(input_data)

        assert result["created"] == len(api_data)
        assert result["updated"] == 0

    async def test_execute_updates_documents_when_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_concours_documents,
        test_app_config,
        httpx_mock,
    ):
        raw_data = copy.deepcopy(raw_concours_documents)
        create_test_documents(
            documents_ingestion_container, raw_data, doc_type=DocumentType.METIERS
        )

        api_response = IngresMetiersApiResponseFactory.build()
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
            url=f"{test_app_config.ingres_base_url}/RMFP_EMPL_REF",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": api_data},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.METIERS},
        )
        result = await documents_usecase.execute(input_data)
        assert result["created"] == len(api_data)
        assert result["updated"] == 0


class TestGeneralDocumentsUsecase:
    async def test_execute_returns_correct_count_with_documents_with_data_input(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_concours_documents,
    ):
        raw_data = copy.deepcopy(raw_concours_documents)
        documents = create_test_documents(documents_ingestion_container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.UPLOAD_FROM_CSV,
            kwargs={"documents": documents, "document_type": DocumentType.CORPS},
        )
        result = await documents_usecase.execute(input_data)
        assert result["updated"] == len(raw_concours_documents)
