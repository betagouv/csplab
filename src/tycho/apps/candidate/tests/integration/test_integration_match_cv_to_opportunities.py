"""Integration tests for MatchCVToOpportunitiesUsecase with external adapters."""

from datetime import datetime
from uuid import uuid4

import pytest
from django.test import TransactionTestCase
from pydantic import HttpUrl

from apps.candidate.containers import CandidateContainer
from apps.candidate.infrastructure.adapters.repositories.cv_metadata_repository import (
    PostgresCVMetadataRepository,
)
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from apps.shared.infrastructure.adapters.persistence.repositories import (
    django_concours_repository as django_concours_repo,
)
from apps.shared.infrastructure.adapters.persistence.repositories import (
    pgvector_repository as pgvector_repo,
)
from apps.shared.tests.fixtures.fixture_loader import load_fixture
from apps.shared.tests.utils.mock_embedding_generator import MockEmbeddingGenerator
from core.errors.cv_errors import CVNotFoundError
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry
from core.value_objects.nor import NOR
from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument


class TestIntegrationMatchCVToOpportunitiesUsecase(TransactionTestCase):
    """Integration test cases for MatchCVToOpportunitiesUsecase with Django."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        super().setUpClass()
        cls.embedding_fixtures = load_fixture("embedding_fixtures.json")

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

        # Override with Django repositories
        django_concours_repository = django_concours_repo.DjangoConcoursRepository()
        self.shared_container.concours_repository.override(django_concours_repository)

        pgvector_repository = pgvector_repo.PgVectorRepository()
        self.shared_container.vector_repository.override(pgvector_repository)

        postgres_cv_metadata_repository = PostgresCVMetadataRepository()
        self.container.cv_metadata_repository.override(postgres_cv_metadata_repository)

        mock_embedding_generator = MockEmbeddingGenerator(self.embedding_fixtures)
        self.shared_container.embedding_generator.override(mock_embedding_generator)

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        self.match_cv_to_opportunities_usecase = (
            self.container.match_cv_to_opportunities_usecase()
        )

    def _create_test_data(self):
        """Create test CVMetadata, Concours and vectorized documents in database."""
        cv_metadata_repository = self.container.cv_metadata_repository()
        concours_repository = self.shared_container.concours_repository()
        vector_repository = self.shared_container.vector_repository()

        # Create test CV metadata
        cv_id = uuid4()
        search_query = list(self.embedding_fixtures.values())[0]["long_label"]
        cv_metadata = CVMetadata(
            id=cv_id,
            filename="test_cv.pdf",
            extracted_text={"experiences": ["Developer"]},
            search_query=search_query,
            created_at=datetime.now(),
        )
        cv_metadata_repository.save(cv_metadata)

        # Create test concours with valid NOR format
        valid_nors = ["MENA2400001A", "AGRI2400002B", "INTE2400003C"]
        concours_list = []
        for i, (concours_id, _) in enumerate(list(self.embedding_fixtures.items())[:3]):
            nor_value = valid_nors[i] if i < len(valid_nors) else f"TEST240000{i + 1}A"
            concours = Concours(
                id=int(concours_id),
                nor_original=NOR(nor_value),
                nor_list=[NOR(nor_value)],
                category=Category.A,
                ministry=Ministry.MAA,
                access_modality=[AccessModality.CONCOURS_EXTERNE],
                corps=f"Corps {concours_id}",
                grade=f"Grade {concours_id}",
                written_exam_date=datetime.now(),
                open_position_number=10,
            )
            concours_list.append(concours)

        result = concours_repository.upsert_batch(concours_list)
        if result["errors"]:
            raise Exception(f"Failed to save Concours entities: {result['errors']}")

        # Create vectorized documents for concours
        for concours in concours_list:
            fixture_data = self.embedding_fixtures[str(concours.id)]
            vectorized_doc = VectorizedDocument(
                id=None,  # Let database assign ID
                document_id=concours.id,
                document_type=DocumentType.CONCOURS,
                content=fixture_data["long_label"],
                embedding=fixture_data["embedding"],
                metadata={"source": "test"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            vector_repository.store_embedding(vectorized_doc)

        # Create some non-concours documents to test filtering
        corps_doc = VectorizedDocument(
            id=None,
            document_id=9999,
            document_type=DocumentType.CORPS,
            content="Test corps document",
            embedding=[0.1] * 3072,  # Mock embedding
            metadata={"source": "test"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        vector_repository.store_embedding(corps_doc)

        return cv_metadata, concours_list

    @pytest.mark.django_db
    def test_execute_with_valid_cv_id_returns_ordered_concours(self):
        """Test that a valid CV ID returns Concours with scores using real database."""
        cv_metadata, concours_list = self._create_test_data()

        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=10
        )

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 3)  # We created 3 concours

        # Check result structure
        for concours, score in result:
            self.assertIsInstance(concours, Concours)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

        # Verify returned concours are from our test data
        returned_ids = {concours.id for concours, score in result}
        expected_ids = {concours.id for concours in concours_list}
        self.assertTrue(returned_ids.issubset(expected_ids))

    @pytest.mark.django_db
    def test_execute_with_invalid_cv_id_raises_cv_not_found_error(self):
        """Test that invalid CV ID raises CVNotFoundError with real database."""
        self._create_test_data()

        invalid_cv_id = str(uuid4())

        with self.assertRaises(CVNotFoundError) as context:
            self.match_cv_to_opportunities_usecase.execute(invalid_cv_id, limit=10)

        self.assertEqual(context.exception.cv_id, invalid_cv_id)

    @pytest.mark.django_db
    def test_execute_filters_only_concours_documents(self):
        """Test that only CONCOURS documents are returned, not CORPS or other types."""
        cv_metadata, concours_list = self._create_test_data()

        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=10
        )

        # Verify we have results and they are all Concours (filtering worked)
        self.assertGreater(len(result), 0)
        for concours, _ in result:
            self.assertIsInstance(concours, Concours)

    @pytest.mark.django_db
    def test_execute_respects_limit_parameter(self):
        """Test that the limit parameter is respected with real database."""
        cv_metadata, concours_list = self._create_test_data()

        # Test with limit smaller than available concours
        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=2
        )
        self.assertLessEqual(len(result), 2)

        # Test with limit larger than available concours
        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=10
        )
        self.assertLessEqual(len(result), len(concours_list))

    @pytest.mark.django_db
    def test_execute_with_no_matching_concours_returns_empty_list(self):
        """Test that when no concours match, empty list is returned."""
        cv_metadata_repository = self.container.cv_metadata_repository()

        # Create CV metadata but no concours
        cv_id = uuid4()
        cv_metadata = CVMetadata(
            id=cv_id,
            filename="empty_test_cv.pdf",
            extracted_text={"skills": [], "experiences": []},
            search_query="non-matching query",
            created_at=datetime.now(),
        )
        cv_metadata_repository.save(cv_metadata)

        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=10
        )

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    @pytest.mark.django_db
    def test_execute_with_no_vectorized_documents_returns_empty_list(self):
        """Test query with no matching vectorized documents returns empty list."""
        cv_metadata_repository = self.container.cv_metadata_repository()

        # Create CV metadata but no vectorized documents
        cv_id = uuid4()
        cv_metadata = CVMetadata(
            id=cv_id,
            filename="no_vectors_cv.pdf",
            extracted_text={"skills": ["Python"], "experiences": ["Developer"]},
            search_query="some random query",
            created_at=datetime.now(),
        )
        cv_metadata_repository.save(cv_metadata)

        result = self.match_cv_to_opportunities_usecase.execute(
            str(cv_metadata.id), limit=10
        )

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
