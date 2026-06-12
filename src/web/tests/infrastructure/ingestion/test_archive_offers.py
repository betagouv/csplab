import re
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from django.conf import settings

from config.app_config import AppConfig
from domain.ingestion.entities.document import DocumentType
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.external_gateways.external_document_gateway import MAX_OFFSET
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.ingestion.talentsoft_factories import (
    TalentsoftBackVacanciesResponseFactory,
    TalentsoftBackVacancyFactory,
)
from tests.factories.ingestion.vectorized_document_factory import (
    VectorizedDocumentFactory,
)
from tests.factories.referentiel.offer_factory import OfferFactory
from tests.infrastructure.ingestion.external_gateways.utils import cached_token
from tests.utils.shared_fixtures import create_shared_qdrant_repository


@pytest.fixture
def documents_integration_container(db):
    shared_qdrant_repository = create_shared_qdrant_repository()
    container = IngestionContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    shared_container.vector_repository.override(shared_qdrant_repository)
    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


@pytest.fixture(name="client")
def authenticated_talentsoft_back_client_fixture(documents_integration_container):
    client = documents_integration_container.talentsoft_back_client()
    client.cached_token = cached_token()
    yield client


TO_ARCHIVE = 1
UNKNOWN = 2
ARCHIVED = 3
ACTIVE = 4


def mock_talentsoft_back_response(
    httpx_mock,
    client,
    mock_data: list | None = None,
    mock_contentRange: str = "0-100/0",
    status_code: int = 200,
):
    url = re.compile(rf"{re.escape(str(client.base_url))}/api/v1/vacancies")
    mock_response = TalentsoftBackVacanciesResponseFactory.build(
        data=mock_data if mock_data else [],
        contentRange=mock_contentRange,
    )
    httpx_mock.add_response(
        method="GET",
        url=url,
        json=mock_response.model_dump(by_alias=True),
        status_code=status_code,
    )


class TestArchiveOffers:
    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_regular_archive_offers(
        self,
        documents_integration_container,
        client,
        httpx_mock,
    ):
        vacancies_to_archive = TalentsoftBackVacancyFactory.batch(TO_ARCHIVE)
        unknown_vacancies = TalentsoftBackVacancyFactory.batch(UNKNOWN)
        archived_vacancies = TalentsoftBackVacancyFactory.batch(ARCHIVED)
        mock_data = vacancies_to_archive + unknown_vacancies + archived_vacancies
        mock_contentRange = f"0-100/{TO_ARCHIVE + UNKNOWN + ARCHIVED}"

        offers_to_archive = [
            OfferFactory.create_model(
                external_id=f"{vacancy.salaryRange.id}-{vacancy.reference}"
            )
            for vacancy in vacancies_to_archive
        ]
        archived_offers = [
            OfferFactory.create_model(
                external_id=f"{vacancy.salaryRange.id}-{vacancy.reference}",
                archived_at=datetime.now(),
            )
            for vacancy in archived_vacancies
        ]
        active_offers = OfferFactory.create_model_batch(ACTIVE)
        offers = offers_to_archive + active_offers

        vector_repo = documents_integration_container.vector_repository()
        vectorized_docs = [
            VectorizedDocumentFactory.create_entity(entity_id=offer.id)
            for offer in offers
        ]
        vector_repo.upsert_batch(vectorized_docs, DocumentType.OFFERS)

        mock_talentsoft_back_response(httpx_mock, client, mock_data, mock_contentRange)

        result = documents_integration_container.archive_offers_usecase().execute(
            updated_after=datetime.now()
        )

        assert result == {
            "fetched": TO_ARCHIVE + UNKNOWN + ARCHIVED,
            "vector_deleted": TO_ARCHIVE,
            "entity_archived": TO_ARCHIVE,
            "errors": [],
        }

        active_offer_models = OfferModel.objects.filter(
            archived_at__isnull=True, id__in=[o.id for o in active_offers]
        )
        assert active_offer_models.count() == ACTIVE

        archived_offers_models = OfferModel.objects.filter(
            archived_at__isnull=False,
            id__in=[o.id for o in offers_to_archive + archived_offers],
        )
        assert archived_offers_models.count() == TO_ARCHIVE + ARCHIVED

        search_results = vector_repo.semantic_search(
            query_embedding=[0.1] * settings.EMBEDDING_DIMENSION,
            limit=10,
            filters={"document_type": DocumentType.OFFERS.value},
        )
        assert len(search_results) == ACTIVE
        vector_set = {s.document.entity_id for s in search_results}
        active_set = {o.id for o in active_offers}
        assert vector_set == active_set

    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_returns_all_documents_over_iteration(
        self,
        documents_integration_container,
        client,
        httpx_mock,
    ):
        iterations = [2, 2, 1]
        for i, count in enumerate(iterations):
            mock_data = TalentsoftBackVacancyFactory.batch(count)
            mock_contentRange = f"{2 * i}-2/5"
            mock_talentsoft_back_response(
                httpx_mock, client, mock_data, mock_contentRange
            )

        result = documents_integration_container.archive_offers_usecase().execute(
            updated_after=datetime.now()
        )

        assert result == {
            "fetched": sum(iterations),
            "vector_deleted": 0,
            "entity_archived": 0,
            "errors": [],
        }

    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_get_archived_documents_max_offset(
        self,
        documents_integration_container,
        client,
        httpx_mock,
    ):
        mock_data = TalentsoftBackVacancyFactory.batch(2)
        mock_contentRange = f"{MAX_OFFSET}-100/{MAX_OFFSET * 2}"
        mock_talentsoft_back_response(httpx_mock, client, mock_data, mock_contentRange)

        result = documents_integration_container.archive_offers_usecase().execute(
            updated_after=datetime.now()
        )
        assert MAX_OFFSET == 100000  # noqa
        assert result == {
            "fetched": 2,
            "vector_deleted": 0,
            "entity_archived": 0,
            "errors": [],
        }

    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_get_vacancies_raises_error(
        self,
        documents_integration_container,
        client,
        httpx_mock,
    ):
        vacancy_without_reference = TalentsoftBackVacancyFactory.build()
        vacancy_without_reference.reference = None
        mock_data = [vacancy_without_reference]
        mock_contentRange = "0-100/1"
        mock_talentsoft_back_response(httpx_mock, client, mock_data, mock_contentRange)

        with pytest.raises(Exception, match="Invalid response structure"):
            documents_integration_container.archive_offers_usecase().execute(
                updated_after=datetime.now()
            )

    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_get_vacancies_returns_empty_list(
        self, documents_integration_container, client, httpx_mock
    ):
        mock_talentsoft_back_response(httpx_mock, client)

        result = documents_integration_container.archive_offers_usecase().execute(
            updated_after=datetime.now()
        )

        assert result == {
            "fetched": 0,
            "vector_deleted": 0,
            "entity_archived": 0,
            "errors": [],
        }

    @pytest.mark.httpx_mock(
        should_mock=lambda request: "talentsoft" in str(request.url)
    )
    def test_delete_vectorized_documents_returns_an_error(
        self,
        documents_integration_container,
        client,
        httpx_mock,
    ):
        num_vacancies = 2
        vacancies = TalentsoftBackVacancyFactory.batch(num_vacancies)
        mock_data = vacancies
        mock_contentRange = f"0-100/{num_vacancies}"

        offers = [
            OfferFactory.create_model(
                external_id=f"{vacancy.salaryRange.id}-{vacancy.reference}"
            )
            for vacancy in vacancies
        ]

        shared_container = documents_integration_container.shared_container()
        vector_repo = shared_container.vector_repository()
        vector_repo.client.delete = MagicMock(side_effect=Exception("Qdrant error"))

        mock_talentsoft_back_response(httpx_mock, client, mock_data, mock_contentRange)

        result = documents_integration_container.archive_offers_usecase().execute(
            updated_after=datetime.now()
        )

        assert result["fetched"] == num_vacancies
        assert result["vector_deleted"] == 0
        assert result["entity_archived"] == num_vacancies
        assert len(result["errors"]) == num_vacancies
        assert all(e["error"] == "Qdrant error" for e in result["errors"])
        assert {e["entity_id"] for e in result["errors"]} == {o.id for o in offers}
