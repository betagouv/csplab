"""Integration tests for VectorizeDocuments usecase with external adapters."""

import json
from pathlib import Path

import pytest
from django.test import TransactionTestCase
from pydantic import HttpUrl

from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.persistence.models import (
    vectorized_document,
)
from apps.ingestion.tests.utils.mock_embedding_generator import MockEmbeddingGenerator
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from apps.shared.infrastructure.adapters.persistence.repositories import (
    django_corps_repository as django_corps_repo,
)
from apps.shared.infrastructure.adapters.persistence.repositories import (
    pgvector_repository as pgvector_repo,
)
from core.entities.corps import Corps
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


class TestIntegrationVectorizeDocumentsUsecase(TransactionTestCase):
    """Integration test cases for VectorizeDocuments usecase with Django persistence."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        super().setUpClass()
        embedding_fixture_data = cls._load_fixture("embedding_fixtures.json")
        cls.embedding_fixtures = embedding_fixture_data

    @classmethod
    def _load_fixture(cls, filename):
        """Load fixture from the shared fixtures directory."""
        fixtures_path = Path(__file__).parent.parent / "fixtures" / filename
        with open(fixtures_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def setUp(self):
        """Set up container dependencies."""
        # Create shared container and config
        self.shared_container = SharedContainer()
        self.shared_config = SharedConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://api.openai.com/v1"),
                model="text-embedding-3-large",
            )
        )
        self.shared_container.config.override(self.shared_config)

        # Create ingestion container
        self.container = IngestionContainer()
        self.ingestion_config = IngestionConfig(
            piste_config=PisteConfig(
                oauth_base_url=HttpUrl("https://fake-piste-oauth.example.com"),
                ingres_base_url=HttpUrl("https://fake-ingres-api.example.com/path"),
                client_id="fake-client-id",
                client_secret="fake-client-secret",  # noqa
            )
        )
        self.container.config.override(self.ingestion_config)
        self.container.shared_container.override(self.shared_container)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)
        http_client = HttpClient()
        self.container.http_client.override(http_client)

        django_corps_repository = django_corps_repo.DjangoCorpsRepository()
        self.shared_container.corps_repository.override(django_corps_repository)

        pgvector_repository = pgvector_repo.PgVectorRepository()
        self.shared_container.vector_repository.override(pgvector_repository)

        # Override embedding generator with mock
        mock_embedding_generator = MockEmbeddingGenerator(self.embedding_fixtures)
        self.shared_container.embedding_generator.override(mock_embedding_generator)

        self.vectorize_documents_usecase = self.container.vectorize_documents_usecase()

    def _create_corps_entities_and_save(self):
        """Create Corps entities with proper value objects and save via repository."""
        corps_repository = self.shared_container.corps_repository()

        corps_1 = Corps(
            id=3,
            code="00003",
            category=Category.A,
            ministry=Ministry.MAA,
            diploma=Diploma(5),
            access_modalities=[
                AccessModality.CONCOURS_EXTERNE,
                AccessModality.CONCOURS_INTERNE,
            ],
            label=Label(
                short_value="PROF LYCE PROF AGRI",
                value="Professeurs de lycée professionnel agricole",
            ),
        )

        corps_2 = Corps(
            id=4,
            code="00004",
            category=Category.A,
            ministry=Ministry.MESRI,
            diploma=Diploma(7),
            access_modalities=[AccessModality.CONCOURS_EXTERNE],
            label=Label(
                short_value="DIRE ETUD EHESS",
                value="Directeurs d'études de l'Ecole",
            ),
        )

        result = corps_repository.upsert_batch([corps_1, corps_2])

        if result["errors"]:
            raise Exception(f"Failed to save Corps entities: {result['errors']}")

        return [corps_1, corps_2]

    @pytest.mark.django_db
    def test_vectorize_corps(self):
        """Test vectorizing Corps with real database and mocked embedding generator."""
        corps_entities = self._create_corps_entities_and_save()

        result = self.vectorize_documents_usecase.execute(corps_entities)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["vectorized"], 2)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(len(result["error_details"]), 0)

        saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
        self.assertEqual(saved_vectors.count(), 2)

        vector_1 = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=3
        )
        vector_2 = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=4
        )

        self.assertIsNotNone(vector_1.embedding)
        self.assertIsNotNone(vector_2.embedding)
        self.assertGreater(len(vector_1.embedding), 0)
        self.assertGreater(len(vector_2.embedding), 0)

        self.assertIn("Professeurs de lycée professionnel agricole", vector_1.content)
        self.assertIn("Directeurs d'études de l'Ecole", vector_2.content)

        self.assertIsNotNone(vector_1.metadata)
        self.assertIsNotNone(vector_2.metadata)

    @pytest.mark.django_db
    def test_vectorize_empty_corps_list(self):
        """Test that empty Corps list is handled correctly."""
        result = self.vectorize_documents_usecase.execute([])

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["vectorized"], 0)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(len(result["error_details"]), 0)

        saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
        self.assertEqual(saved_vectors.count(), 0)

    @pytest.mark.django_db
    def test_vectorize_corps_updates_existing_document(self):
        """Test that vectorizing the same Corps twice updates the existing document."""
        corps_entities = self._create_corps_entities_and_save()

        result1 = self.vectorize_documents_usecase.execute([corps_entities[0]])

        self.assertEqual(result1["processed"], 1)
        self.assertEqual(result1["vectorized"], 1)
        self.assertEqual(result1["errors"], 0)

        saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
        self.assertEqual(saved_vectors.count(), 1)

        first_vector = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=3
        )
        original_created_at = first_vector.created_at
        original_updated_at = first_vector.updated_at

        result2 = self.vectorize_documents_usecase.execute([corps_entities[0]])

        self.assertEqual(result2["processed"], 1)
        self.assertEqual(result2["vectorized"], 1)
        self.assertEqual(result2["errors"], 0)

        saved_vectors = vectorized_document.VectorizedDocumentModel.objects.all()
        self.assertEqual(saved_vectors.count(), 1)

        updated_vector = vectorized_document.VectorizedDocumentModel.objects.get(
            document_id=3
        )

        self.assertEqual(updated_vector.created_at, original_created_at)
        self.assertGreater(updated_vector.updated_at, original_updated_at)

        self.assertIsNotNone(updated_vector.embedding)
        self.assertGreater(len(updated_vector.embedding), 0)
        self.assertIn(
            "Professeurs de lycée professionnel agricole", updated_vector.content
        )
