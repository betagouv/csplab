"""Unit test cases for LoadDocuments documents_usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the documents_usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import copy
from datetime import datetime, timezone

import pytest
import responses

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from infrastructure.exceptions.ingestion_exceptions import (
    MissingOperationParameterError,
)
from tests.external_gateways.utils import cached_token, offers_response
from tests.factories.ingres_factories import IngresCorpsApiResponseFactory


@pytest.fixture(name="corps_document")
def corps_document_fixture():
    """Create a single corps document for testing."""
    return Document(
        external_id="test_corps_doc",
        raw_data={"name": "Test Document"},
        type=DocumentType.CORPS,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture(name="corps_documents")
def corps_documents_fixture():
    """Create multiple corps documents for batch testing."""
    return [
        Document(
            external_id="corps_1",
            raw_data={"name": "Corps 1", "description": "First corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        Document(
            external_id="corps_2",
            raw_data={"name": "Corps 2", "description": "Second corps"},
            type=DocumentType.CORPS,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]


@pytest.fixture(name="offer_documents")
def offer_documents_fixture():
    """Create multiple offer documents for batch testing."""
    return [
        Document(
            external_id="offer_1",
            raw_data={"name": "Offer 1", "description": "First offer"},
            type=DocumentType.OFFERS,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        Document(
            external_id="offer_2",
            raw_data={"name": "Offer 2", "description": "Second offer"},
            type=DocumentType.OFFERS,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]


@pytest.fixture(name="raw_offer_documents")
def raw_offer_documents_fixture(offer_documents):
    """Return raw_data of offer_documents fixture."""
    return [doc.raw_data for doc in offer_documents]


@pytest.fixture(name="concours_documents")
def concours_documents_fixture():
    """Create sample contest documents."""
    return [
        Document(
            external_id="exam_1",
            raw_data={"name": "Exam 1"},
            type=DocumentType.CONCOURS,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]


@pytest.fixture(name="raw_concours_documents")
def raw_concours_documents_fixture(concours_documents):
    """Return raw_data of concours_documents fixture."""
    return [doc.raw_data for doc in concours_documents]


def create_test_documents(
    documents_ingestion_container,
    raw_data_list,
    doc_type=DocumentType.CORPS,
):
    """Helper to create test documents and load them into documents_repository."""
    documents_repository = documents_ingestion_container.document_repository()

    documents = [
        Document(
            external_id=f"test_doc_{i}",
            raw_data={"test": "data", "index": i},
            type=doc_type,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for i, _raw_data in enumerate(raw_data_list)
    ]

    documents_repository.upsert_batch(documents, doc_type.value)
    return documents


class TestCorpsDocumentsUsecase:
    """Test documents usecase for CORPS documents."""

    @responses.activate
    def test_execute_returns_zero_when_no_documents(
        self, documents_usecase, piste_gateway_config
    ):
        """Test execute returns 0 when documents_repository is empty."""
        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": []},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    @responses.activate
    def test_execute_creates_new_documents_when_none_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        piste_gateway_config,
    ):
        """Test execute creates new documents when none exist in the system."""
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)

        assert result["created"] == len(api_data)
        assert result["updated"] == 0

    @responses.activate
    def test_execute_updates_documents_when_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_concours_documents,
        piste_gateway_config,
    ):
        """Test execute updates existing documents."""
        raw_data = copy.deepcopy(raw_concours_documents)
        create_test_documents(
            documents_ingestion_container, raw_data, doc_type=DocumentType.CORPS
        )

        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == len(api_data)
        assert result["updated"] == 0


class TestOffersDocumentsUsecase:
    """Test documents usecase for OFFERS documents."""

    def test_execute_returns_zero_when_no_documents(
        self, documents_usecase, documents_ingestion_container, httpx_mock
    ):
        """Test execute returns 0 when documents_repository is empty."""
        client = documents_ingestion_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=offers_response(count=0),
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    def test_execute_creates_new_documents_when_none_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        httpx_mock,
    ):
        """Test execute creates new documents when none exist in the system."""
        count = 2
        client = documents_ingestion_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=offers_response(count=count),
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = documents_usecase.execute(input_data)

        assert result["created"] == count
        assert result["updated"] == 0

    def test_execute_updates_documents_when_exist(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_offer_documents,
        httpx_mock,
    ):
        """Test execute updates existing documents."""
        raw_data = copy.deepcopy(raw_offer_documents)
        create_test_documents(
            documents_ingestion_container, raw_data, doc_type=DocumentType.OFFERS
        )

        count = 2
        client = documents_ingestion_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=offers_response(count=count),
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = documents_usecase.execute(input_data)
        assert result["created"] == count
        assert result["updated"] == 0


class TestGeneralDocumentsUsecase:
    """Test general documents usecase functionality."""

    def test_execute_returns_correct_count_with_documents_with_data_input(
        self,
        documents_usecase,
        documents_ingestion_container,
        raw_concours_documents,
    ):
        """Test execute returns correct count when documents exist with CSV upload."""
        raw_data = copy.deepcopy(raw_concours_documents)
        documents = create_test_documents(documents_ingestion_container, raw_data)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.UPLOAD_FROM_CSV,
            kwargs={"documents": documents, "document_type": DocumentType.CORPS},
        )
        result = documents_usecase.execute(input_data)
        assert result["updated"] == len(raw_concours_documents)

    def test_missing_document_type_raises_missing_operation_parameter_error(
        self, documents_usecase
    ):
        """Test that missing document_type in kwargs raises ApplicationError."""
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={},
        )
        with pytest.raises(MissingOperationParameterError):
            documents_usecase.execute(input_data)
