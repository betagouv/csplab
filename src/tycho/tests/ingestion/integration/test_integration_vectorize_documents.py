"""Integration tests for VectorizeDocuments usecase with external adapters."""

import pytest
from django.test import TransactionTestCase
from pydantic import HttpUrl

from domain.entities.corps import Corps
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models import vectorized_document
from infrastructure.external_gateways.configs.openai_config import (
    OpenAIConfig,
    OpenAIGatewayConfig,
)
from infrastructure.external_gateways.configs.piste_config import (
    PisteConfig,
    PisteGatewayConfig,
)
from infrastructure.external_gateways.http_client import HttpClient
from infrastructure.external_gateways.logger import LoggerService
from infrastructure.repositories.shared import pgvector_repository as pgvector_repo
from infrastructure.repositories.shared import (
    postgres_corps_repository as postgres_corps_repo,
)
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator


class TestIntegrationVectorizeDocumentsUsecase(TransactionTestCase):
    """Integration test cases for VectorizeDocuments usecase with Django persistence."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        super().setUpClass()
        cls.embedding_fixtures = load_fixture("embedding_fixtures.json")

    def setUp(self):
        """Set up container dependencies."""
        # Create shared container and config
        self.shared_container = SharedContainer()
        self.openai_gateway_config = OpenAIGatewayConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://api.openai.com/v1"),
                model="text-embedding-3-large",
            )
        )
        self.shared_container.config.override(self.openai_gateway_config)

        # Create ingestion container
        self.container = IngestionContainer()
        self.piste_gateway_config = PisteGatewayConfig(
            piste_config=PisteConfig(
                oauth_base_url=HttpUrl("https://fake-piste-oauth.example.com"),
                ingres_base_url=HttpUrl("https://fake-ingres-api.example.com/path"),
                client_id="fake-client-id",
                client_secret="fake-client-secret",  # noqa
            )
        )
        self.container.config.override(self.piste_gateway_config)
        self.container.shared_container.override(self.shared_container)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)
        http_client = HttpClient()
        self.container.http_client.override(http_client)

        postgres_corps_repository = postgres_corps_repo.PostgresCorpsRepository()
        self.shared_container.corps_repository.override(postgres_corps_repository)

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
