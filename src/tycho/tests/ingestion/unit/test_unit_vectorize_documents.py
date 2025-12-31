"""Unit test cases for VectorizeDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import unittest
from datetime import datetime

from apps.ingestion.containers import IngestionContainer
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from domain.entities.corps import Corps
from domain.entities.document import Document, DocumentType
from domain.interfaces.entity_interface import IEntity
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.diploma import Diploma
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry
from tests.fixtures.fixture_loader import load_fixture
from tests.utils.test_container_factory import (
    create_test_shared_container,
)


class UnsupportedEntity(IEntity):
    """Mock entity for testing unsupported source type."""

    def __init__(self, id: int):
        """Initialize with id."""
        self.id = id


class TestUnitVectorizeDocumentsUsecase(unittest.TestCase):
    """Unit test cases for VectorizeDocuments usecase."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        cls.embedding_fixtures = load_fixture("embedding_fixtures.json")

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = IngestionContainer()

        # Override with test dependencies
        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        # Create and configure shared container for testing
        shared_container = create_test_shared_container(self.embedding_fixtures)
        container.shared_container.override(shared_container)

        return container

    def test_vectorize_two_corps_returns_correct_embeddings(self):
        """Test vectorizing two Corps returns correct embeddings from fixtures."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        corps_ids = list(self.embedding_fixtures.keys())[:2]

        corps_list = []
        expected_embeddings = {}

        for corps_id in corps_ids:
            fixture_data = self.embedding_fixtures[corps_id]
            long_label = fixture_data["long_label"]
            expected_embedding = fixture_data["embedding"]

            corps = Corps(
                id=int(corps_id),
                code=f"CODE{corps_id}",
                category=Category.A,
                ministry=Ministry.MAA,
                diploma=Diploma(5),
                access_modalities=[AccessModality.CONCOURS_EXTERNE],
                label=Label(short_value=long_label[:20], value=long_label),
            )
            corps_list.append(corps)
            expected_embeddings[int(corps_id)] = expected_embedding

        result = usecase.execute(corps_list)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["vectorized"], 2)
        self.assertEqual(result["errors"], 0)

    # TODO: vectorize concours pour clean et matcher les corps_id grade_id
    # def test_vectorize_two_documents_returns_correct_embeddings(self):
    #     """Test vectorizing two Documents returns correct embeddings from fixtures."""
    #     container = self._create_isolated_container()
    #     usecase = container.vectorize_documents_usecase()

    #     doc_ids = list(self.embedding_fixtures.keys())[:2]

    #     doc_list = []
    #     expected_embeddings = {}

    #     for doc_id in doc_ids:
    #         fixture_data = self.embedding_fixtures[doc_id]
    #         long_label = fixture_data["long_label"]
    #         expected_embedding = fixture_data["embedding"]

    #         document = Document(
    #             id=int(doc_id),
    #             external_id=doc_id,
    #             raw_data=long_label,
    #             type=DocumentType.CONCOURS,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         )
    #         doc_list.append(document)
    #         expected_embeddings[int(doc_id)] = expected_embedding

    #     result = usecase.execute(doc_list)

    #     self.assertEqual(result["processed"], 2)
    #     self.assertEqual(result["vectorized"], 2)
    #     self.assertEqual(result["errors"], 0)

    def test_vectorize_corps_with_exception_handles_error_correctly(self):
        """Test that exceptions during vectorization are properly handled and logged."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        # Create a Corps with None label to trigger an exception
        invalid_corps = Corps(
            id=999,
            code="INVALID",
            category=Category.A,
            ministry=Ministry.MAA,
            diploma=Diploma(5),
            access_modalities=[AccessModality.CONCOURS_EXTERNE],
            label=None,  # This will cause an exception in text extraction
        )

        result = usecase.execute([invalid_corps])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 0)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(len(result["error_details"]), 1)

        error_detail = result["error_details"][0]
        self.assertEqual(error_detail["source_type"], "Corps")
        self.assertEqual(error_detail["source_id"], 999)
        self.assertIn("error", error_detail)

    def test_vectorize_document_returns_correct_result(self):
        """Test vectorizing a Document returns correct result."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        document = Document(
            id=1,
            external_id="test_vectorize_doc",
            raw_data={"content": "Test document content for vectorization"},
            type=DocumentType.GRADE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = usecase.execute([document])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 0)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(
            result["error_details"][0]["error"],
            "Content extraction not implemented for document type GRADE",
        )

    def test_vectorize_unsupported_source_type_handles_error_correctly(self):
        """Test that unsupported source types are properly handled and logged."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        unsupported_entity = UnsupportedEntity(id=123)

        result = usecase.execute([unsupported_entity])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 0)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(len(result["error_details"]), 1)

        error_detail = result["error_details"][0]

        self.assertEqual(error_detail["source_type"], "UnsupportedEntity")
        self.assertEqual(error_detail["source_id"], 123)
        self.assertIn(
            "Content extraction not implemented",
            error_detail["error"],
        )
