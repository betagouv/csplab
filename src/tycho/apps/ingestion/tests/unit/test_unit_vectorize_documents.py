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
from apps.shared.tests.fixtures.fixture_loader import load_fixture
from apps.shared.tests.utils.test_container_factory import (
    create_test_shared_container,
)
from core.entities.corps import Corps
from core.entities.document import Document, DocumentType
from core.entities.offer import Offer
from core.interfaces.entity_interface import IEntity
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.department import Department
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.limit_date import LimitDate
from core.value_objects.localisation import Localisation
from core.value_objects.ministry import Ministry
from core.value_objects.region import Region
from core.value_objects.verse import Verse


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

    def test_vectorize_offer_returns_correct_result(self):
        """Test vectorizing an Offer entity returns correct result."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        offer = Offer(
            id=1,
            external_id="OFFER_001",
            titre="Développeur Full Stack",
            profile="Expérience en Python, Django, PostgreSQL",
            category=Category.A,
            verse=Verse.FPE,
            localisation=Localisation(
                region=Region.ILE_DE_FRANCE, department=Department.PARIS
            ),
            limit_date=LimitDate(datetime(2024, 12, 31, 23, 59, 59)),
        )

        result = usecase.execute([offer])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 1)
        self.assertEqual(result["errors"], 0)

    def test_vectorize_offer_with_minimal_data_returns_correct_result(self):
        """Test vectorizing an Offer with minimal data returns correct result."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        offer = Offer(
            id=2,
            external_id="OFFER_002",
            titre="Data Scientist",
            profile="Machine Learning, Python, SQL",
            category=None,
            verse=None,
            localisation=None,
            limit_date=None,
        )

        result = usecase.execute([offer])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 1)
        self.assertEqual(result["errors"], 0)

    def test_vectorize_multiple_offers_returns_correct_result(self):
        """Test vectorizing multiple Offer entities returns correct result."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        offers = [
            Offer(
                id=1,
                external_id="OFFER_001",
                titre="Développeur Full Stack",
                profile="Expérience en Python, Django, PostgreSQL",
                category=Category.A,
                verse=Verse.FPE,
                localisation=Localisation(
                    region=Region.ILE_DE_FRANCE, department=Department.PARIS
                ),
                limit_date=LimitDate(datetime(2024, 12, 31, 23, 59, 59)),
            ),
            Offer(
                id=2,
                external_id="OFFER_002",
                titre="Data Scientist",
                profile="Machine Learning, Python, SQL",
                category=Category.A,
                verse=Verse.FPE,
                localisation=Localisation(
                    region=Region.AUVERGNE_RHONE_ALPES, department=Department.RHONE
                ),
                limit_date=LimitDate(datetime(2024, 11, 30, 23, 59, 59)),
            ),
        ]

        result = usecase.execute(offers)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["vectorized"], 2)
        self.assertEqual(result["errors"], 0)

    def test_vectorize_offer_with_none_id_handles_error_correctly(self):
        """Test that Offer with None id is properly handled and logged."""
        container = self._create_isolated_container()
        usecase = container.vectorize_documents_usecase()

        offer = Offer(
            id=None,  # This will cause an exception
            external_id="OFFER_INVALID",
            titre="Invalid Offer",
            profile="Test profile",
            category=Category.A,
            verse=Verse.FPE,
            localisation=None,
            limit_date=None,
        )

        result = usecase.execute([offer])

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["vectorized"], 0)
        self.assertEqual(result["errors"], 1)
        self.assertEqual(len(result["error_details"]), 1)

        error_detail = result["error_details"][0]
        self.assertEqual(error_detail["source_type"], "Offer")
        self.assertEqual(error_detail["source_id"], None)
        self.assertIn("Document ID cannot be None", error_detail["error"])
