"""Unit test cases for MatchCVToOpportunitiesUsecase."""

import unittest
from datetime import datetime
from uuid import uuid4

from apps.candidate.containers import CandidateContainer
from domain.entities.concours import Concours
from domain.entities.cv_metadata import CVMetadata
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.exceptions.cv_errors import CVNotFoundError
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR
from infrastructure.external_services.logger import LoggerService
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.in_memory_concours_repository import (
    InMemoryConcoursRepository,
)
from tests.utils.in_memory_cv_metadata_repository import (
    InMemoryCVMetadataRepository,
)
from tests.utils.test_container_factory import create_test_shared_container


class TestUnitMatchCVToOpportunitiesUsecase(unittest.TestCase):
    """Unit test cases for MatchCVToOpportunitiesUsecase."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        cls.embedding_fixtures = load_fixture("embedding_fixtures.json")

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = CandidateContainer()

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        shared_container = create_test_shared_container(self.embedding_fixtures)
        container.shared_container.override(shared_container)

        # Override with in-memory repositories for testing
        cv_metadata_repository = InMemoryCVMetadataRepository()
        container.cv_metadata_repository.override(cv_metadata_repository)

        concours_repository = InMemoryConcoursRepository()
        shared_container.concours_repository.override(concours_repository)

        return container

    def _setup_test_data(self, container):
        """Setup test CVMetadata, Concours and vectorized documents."""
        cv_metadata_repository = container.cv_metadata_repository()
        concours_repository = container.shared_container.concours_repository()
        vector_repository = container.shared_container.vector_repository()

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

        concours_repository.upsert_batch(concours_list)

        # Create vectorized documents for concours
        for concours in concours_list:
            fixture_data = self.embedding_fixtures[str(concours.id)]
            vectorized_doc = VectorizedDocument(
                id=concours.id,
                document_id=concours.id,  # Links to concours.id
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
            id=9999,
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

    def test_execute_with_valid_cv_id_returns_ordered_concours(self):
        """Test that a valid CV ID returns Concours with scores."""
        container = self._create_isolated_container()
        cv_metadata, concours_list = self._setup_test_data(container)
        usecase = container.match_cv_to_opportunities_usecase()

        result = usecase.execute(str(cv_metadata.id), limit=10)

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

    def test_execute_with_invalid_cv_id_raises_cv_not_found_error(self):
        """Test that invalid CV ID raises CVNotFoundError."""
        container = self._create_isolated_container()
        self._setup_test_data(container)
        usecase = container.match_cv_to_opportunities_usecase()

        invalid_cv_id = str(uuid4())

        with self.assertRaises(CVNotFoundError) as context:
            usecase.execute(invalid_cv_id, limit=10)

        self.assertEqual(context.exception.cv_id, invalid_cv_id)

    def test_execute_respects_limit_parameter(self):
        """Test that the limit parameter is respected."""
        container = self._create_isolated_container()
        cv_metadata, concours_list = self._setup_test_data(container)
        usecase = container.match_cv_to_opportunities_usecase()

        # Test with limit smaller than available concours
        result = usecase.execute(str(cv_metadata.id), limit=2)
        self.assertLessEqual(len(result), 2)

        # Test with limit larger than available concours
        result = usecase.execute(str(cv_metadata.id), limit=10)
        self.assertLessEqual(len(result), len(concours_list))

    def test_execute_with_no_matching_concours_returns_empty_list(self):
        """Test that when no concours match, empty list is returned."""
        container = self._create_isolated_container()
        cv_metadata_repository = container.cv_metadata_repository()
        usecase = container.match_cv_to_opportunities_usecase()

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

        result = usecase.execute(str(cv_metadata.id), limit=10)

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
