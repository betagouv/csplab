"""Integration tests for RetrieveCorpsUsecase with external adapters."""

import json
from datetime import datetime
from pathlib import Path

import pytest
from django.test import TransactionTestCase
from pydantic import HttpUrl

from apps.candidate.containers import CandidateContainer
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from apps.shared.infrastructure.adapters.persistence.repositories import (
    django_corps_repository as django_corps_repo,
)
from apps.shared.infrastructure.adapters.persistence.repositories import (
    pgvector_repository as pgvector_repo,
)
from apps.shared.tests.utils.mock_embedding_generator import MockEmbeddingGenerator
from core.entities.corps import Corps
from core.entities.document import DocumentType
from core.entities.vectorized_document import VectorizedDocument
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


class TestIntegrationRetrieveCorpsUsecase(TransactionTestCase):
    """Integration test cases for RetrieveCorpsUsecase with Django persistence."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        super().setUpClass()
        cls.embedding_fixtures = cls._load_fixture("embedding_fixtures.json")

    @classmethod
    def _load_fixture(cls, filename):
        """Load fixture from the shared fixtures directory."""
        fixtures_path = Path(__file__).parent.parent / "fixtures" / filename
        with open(fixtures_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def setUp(self):
        """Set up container dependencies."""
        self.shared_container = SharedContainer()
        self.shared_config = SharedConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://api.openai.com/v1"),
                model="text-embedding-3-large",
            )
        )
        self.shared_container.config.override(self.shared_config)

        self.container = CandidateContainer()
        self.container.shared_container.override(self.shared_container)

        django_corps_repository = django_corps_repo.DjangoCorpsRepository()
        self.shared_container.corps_repository.override(django_corps_repository)

        pgvector_repository = pgvector_repo.PgVectorRepository()
        self.shared_container.vector_repository.override(pgvector_repository)

        mock_embedding_generator = MockEmbeddingGenerator(self.embedding_fixtures)
        self.shared_container.embedding_generator.override(mock_embedding_generator)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        self.retrieve_corps_usecase = self.container.retrieve_corps_usecase()

    def _create_test_data(self):
        """Create test Corps and vectorized documents in database."""
        corps_repository = self.shared_container.corps_repository()
        vector_repository = self.shared_container.vector_repository()

        corps_list = []
        for corps_id, fixture_data in list(self.embedding_fixtures.items())[:2]:
            corps = Corps(
                id=int(corps_id),
                code=f"CODE{corps_id}",
                category=Category.A,
                ministry=Ministry.MAA,
                diploma=Diploma(5),
                access_modalities=[AccessModality.CONCOURS_EXTERNE],
                label=Label(
                    short_value=fixture_data["long_label"][:20],
                    value=fixture_data["long_label"],
                ),
            )
            corps_list.append(corps)

        result = corps_repository.upsert_batch(corps_list)
        if result["errors"]:
            raise Exception(f"Failed to save Corps entities: {result['errors']}")

        for corps in corps_list:
            fixture_data = self.embedding_fixtures[str(corps.id)]
            vectorized_doc = VectorizedDocument(
                id=None,  # Let database assign ID
                document_id=corps.id,
                document_type=DocumentType.CORPS,
                content=fixture_data["long_label"],
                embedding=fixture_data["embedding"],
                metadata={"document_type": "CORPS"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            vector_repository.store_embedding(vectorized_doc)

        return corps_list

    @pytest.mark.django_db
    def test_retrieve_corps_with_valid_query_returns_results(self):
        """Test retrieving Corps with valid query using real database."""
        corps_list = self._create_test_data()

        query = list(self.embedding_fixtures.values())[0]["long_label"]

        result = self.retrieve_corps_usecase.execute(query, limit=10)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Corps)

        self.assertEqual(result[0].label.value, query)

        returned_ids = {corps.id for corps in result}
        expected_ids = {corps.id for corps in corps_list}
        self.assertEqual(returned_ids, expected_ids)

    @pytest.mark.django_db
    def test_retrieve_corps_with_empty_query_returns_empty_list(self):
        """Test that empty query returns empty list with real database."""
        self._create_test_data()

        result = self.retrieve_corps_usecase.execute("", limit=10)

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    @pytest.mark.django_db
    def test_retrieve_corps_with_no_matching_documents_returns_empty_list(self):
        """Test query with no matching vectorized documents returns empty list."""
        result = self.retrieve_corps_usecase.execute("some random query", limit=10)

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    @pytest.mark.django_db
    def test_retrieve_corps_respects_limit_parameter(self):
        """Test that limit parameter is respected."""
        self._create_test_data()

        query = list(self.embedding_fixtures.values())[0]["long_label"]

        result = self.retrieve_corps_usecase.execute(query, limit=1)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Corps)
