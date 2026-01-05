"""Unit test cases for RetrieveCorpsUsecase."""

import unittest
from datetime import datetime

from infrastructure.external_gateways.logger import LoggerService

from domain.entities.corps import Corps
from domain.entities.document import DocumentType
from domain.entities.vectorized_document import VectorizedDocument
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry
from infrastructure.di.candidate.candidate_container import CandidateContainer
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.test_container_factory import create_test_shared_container


class TestUnitRetrieveCorpsUsecase(unittest.TestCase):
    """Unit test cases for RetrieveCorpsUsecase."""

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

        return container

    def _setup_test_data(self, container):
        """Setup test Corps and vectorized documents."""
        corps_repository = container.shared_container.corps_repository()
        vector_repository = container.shared_container.vector_repository()

        corps_list = []
        for corps_id, fixture_data in list(self.embedding_fixtures.items())[
            :2
        ]:  # Use first 2 fixtures
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

        corps_repository.upsert_batch(corps_list)

        for corps in corps_list:
            fixture_data = self.embedding_fixtures[str(corps.id)]
            vectorized_doc = VectorizedDocument(
                id=corps.id,
                document_id=corps.id,  # Links to corps.id
                document_type=DocumentType.CORPS,
                content=fixture_data["long_label"],
                embedding=fixture_data["embedding"],
                metadata={"document_type": "CORPS"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            vector_repository.store_embedding(vectorized_doc)

        return corps_list

    def test_execute_with_valid_query_returns_ordered_corps(self):
        """Test that a valid query returns Corps with scores ordered by similarity."""
        container = self._create_isolated_container()
        corps_list = self._setup_test_data(container)
        usecase = container.retrieve_corps_usecase()

        query = list(self.embedding_fixtures.values())[0]["long_label"]

        result = usecase.execute(query, limit=10)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], Corps)
        self.assertIsInstance(result[0][1], float)

        self.assertEqual(result[0][0].label.value, query)

        # Verify scores are between 0 and 1 (relevance scores)
        for _, score in result:
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

        returned_ids = {corps.id for corps, score in result}
        expected_ids = {corps.id for corps in corps_list}
        self.assertEqual(returned_ids, expected_ids)

    def test_execute_with_empty_query_returns_empty_list(self):
        """Test that empty or whitespace query returns empty list."""
        container = self._create_isolated_container()
        self._setup_test_data(container)
        usecase = container.retrieve_corps_usecase()

        result = usecase.execute("", limit=10)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

        result = usecase.execute("   ", limit=10)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

        result = usecase.execute(None or "", limit=10)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
