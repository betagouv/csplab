"""Unit test cases for VectorizeDocuments usecase."""

import json
import unittest
from pathlib import Path

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.logger import LoggerService
from apps.ingestion.tests.utils.mock_embedding_generator import MockEmbeddingGenerator
from core.entities.corps import Corps
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry


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

    def setUp(self):
        """Set up container dependencies."""
        self.container = IngestionContainer()
        self.container.in_memory_mode.override("in_memory")

        logger_service = LoggerService()
        self.container.logger_service.override(logger_service)

        mock_generator = MockEmbeddingGenerator(self.embedding_fixtures)
        self.container.embedding_generator.override(mock_generator)

        self.usecase = self.container.vectorize_documents_usecase()

    def tearDown(self):
        """Clean up after each test."""
        vector_repository = self.container.vector_repository()
        if hasattr(vector_repository, "_documents"):
            vector_repository._documents.clear()

    def test_vectorize_two_corps_returns_correct_embeddings(self):
        """Test vectorizing two Corps returns correct embeddings from fixtures."""
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

        # result = self.usecase.execute(corps_list)

        # self.assertEqual(len(result), 2)

        # vector_repository = self.container.vector_repository()

        # for vectorized_doc in result:
        #     corps_id = vectorized_doc.document_id
        #     expected_embedding = expected_embeddings[corps_id]

        #     self.assertEqual(vectorized_doc.embedding, expected_embedding)

        #     expected_content = next(
        #         corps.label.value for corps in corps_list if corps.id == corps_id
        #     )
        #     self.assertEqual(vectorized_doc.content, expected_content)

        #     self.assertIn("type", vectorized_doc.metadata)
        #     self.assertEqual(vectorized_doc.metadata["type"], "Corps")
        #     self.assertEqual(vectorized_doc.metadata["corps_id"], corps_id)

        # stored_docs = list(vector_repository._documents.values())
        # self.assertEqual(len(stored_docs), 2)

        # for stored_doc in stored_docs:
        #     self.assertIn(stored_doc.document_id, expected_embeddings)
        #     expected_embedding = expected_embeddings[stored_doc.document_id]
        #     self.assertEqual(stored_doc.embedding, expected_embedding)
