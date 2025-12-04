"""Unit test cases for VectorizeDocuments usecase.

IMPORTANT: Dependency Injection Override Timing
- Override timing is crucial with dependency-injector
- Always override BEFORE creating the usecase, not after
- Dependencies are resolved at creation time, not execution time
"""

import json
import unittest
from datetime import datetime
from pathlib import Path

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.logger import LoggerService
from apps.ingestion.tests.utils.in_memory_corps_repository import (
    InMemoryCorpsRepository,
)
from apps.ingestion.tests.utils.in_memory_vector_repository import (
    InMemoryVectorRepository,
)
from apps.ingestion.tests.utils.mock_embedding_generator import MockEmbeddingGenerator
from core.entities.corps import Corps
from core.entities.document import Document, DocumentType
from core.interfaces.entity_interface import IEntity
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


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
        cls.embedding_fixtures = cls._load_fixture("embedding_fixtures.json")

    @classmethod
    def _load_fixture(cls, filename):
        """Load fixture from the shared fixtures directory."""
        fixtures_path = Path(__file__).parent.parent / "fixtures" / filename
        with open(fixtures_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _create_isolated_container(self):
        """Create an isolated container for each test to avoid concurrency issues."""
        container = IngestionContainer()

        # Override with test dependencies
        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        # Override with in-memory repositories for unit tests
        in_memory_corps_repo = InMemoryCorpsRepository()
        container.corps_repository.override(in_memory_corps_repo)

        in_memory_vector_repo = InMemoryVectorRepository()
        container.vector_repository.override(in_memory_vector_repo)

        # Override with mock embedding generator
        mock_generator = MockEmbeddingGenerator(self.embedding_fixtures)
        container.embedding_generator.override(mock_generator)

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
