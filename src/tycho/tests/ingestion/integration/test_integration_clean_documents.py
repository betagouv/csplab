"""Integration tests for CleanDocuments usecase with external adapters."""

import pytest
from django.test import TransactionTestCase
from pydantic import HttpUrl

from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.models.raw_document import (
    RawDocument,
)
from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer
from apps.shared.models.concours import (
    ConcoursModel,
)
from apps.shared.models.corps import CorpsModel
from domain.entities.document import DocumentType
from infrastructure.external_services.http_client import HttpClient
from infrastructure.external_services.logger import LoggerService
from infrastructure.repositories.ingestion import (
    django_document_repository as django_doc_repo,
)
from tests.fixtures.fixture_loader import load_fixture

REFERENCE_YEAR = 2024


class TestIntegrationCleanDocumentsUsecase(TransactionTestCase):
    """Integration test cases for CleanDocuments usecase with Django persistence."""

    @classmethod
    def setUpClass(cls):
        """Load fixtures once for all tests."""
        super().setUpClass()
        cls.raw_corps_documents = load_fixture("corps_ingres_20251117.json")
        cls.raw_concours_documents = load_fixture("concours_greco_2025.json")

    def setUp(self):
        """Set up container dependencies."""
        # Create shared container and config
        self.shared_container = SharedContainer()
        self.shared_config = SharedConfig(
            openai_config=OpenAIConfig(
                api_key="fake-api-key",
                base_url=HttpUrl("https://fake-base-url.example.com"),
                model="fake-model",
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

        django_document_repository = django_doc_repo.DjangoDocumentRepository()
        self.container.document_repository.override(django_document_repository)

        self.clean_documents_usecase = self.container.clean_documents_usecase()

    def _create_raw_documents_in_db(self, raw_data_list, doc_type=DocumentType.CORPS):
        """Create RawDocument entries directly in Django database."""
        for i, raw_data in enumerate(raw_data_list):
            RawDocument.objects.create(
                id=i + 1,
                raw_data=raw_data,
                document_type=doc_type.value,
            )

    def _create_raw_concours_documents_in_db(self, raw_data_list):
        """Create RawDocument entries for CONCOURS type in Django database."""
        self._create_raw_documents_in_db(raw_data_list, DocumentType.CONCOURS)

    @pytest.mark.django_db
    def test_execute_handles_empty_documents(self):
        """Test that empty document list is handled correctly."""
        # No documents in database
        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        # Verify no Corps entities are saved
        saved_corps = CorpsModel.objects.all()
        self.assertEqual(saved_corps.count(), 0)

    @pytest.mark.django_db
    def test_execute_updates_existing_corps(self):
        """Test that existing Corps entities are updated correctly."""
        # Create raw document in database
        valid_corps_data = [self.raw_corps_documents[0]]
        self._create_raw_documents_in_db(valid_corps_data)

        # First execution - create corps
        result1 = self.clean_documents_usecase.execute(DocumentType.CORPS)
        self.assertEqual(result1["created"], 1)
        self.assertEqual(result1["updated"], 0)

        # Second execution with same data - should update
        result2 = self.clean_documents_usecase.execute(DocumentType.CORPS)
        self.assertEqual(result2["created"], 0)
        self.assertEqual(result2["updated"], 1)

        # Verify only one Corps entity exists
        saved_corps = CorpsModel.objects.all()
        self.assertEqual(len(saved_corps), 1)

    @pytest.mark.django_db
    def test_execute_filters_non_fpe_data(self):
        """Test that non-FPE corps data is properly filtered out."""
        # Create mixed data: 1 valid FPE + 1 invalid FPT
        valid_corps_data = self.raw_corps_documents[0].copy()
        invalid_corps_data = self.raw_corps_documents[1].copy()
        invalid_corps_data["corpsOuPseudoCorps"]["caracteristiques"][
            "natureFonctionPublique"
        ]["libelleNatureFoncPub"] = "FPT"

        self._create_raw_documents_in_db([valid_corps_data, invalid_corps_data])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        # Verify statistics - only FPE documents should be cleaned and saved
        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        # Verify only valid Corps is saved
        saved_corps = CorpsModel.objects.all()
        self.assertEqual(saved_corps.count(), 1)

    @pytest.mark.django_db
    def test_execute_retrieves_saved_corps_by_id(self):
        """Test that saved Corps entities can be retrieved by ID."""
        # Create raw document in database
        valid_corps_data = [self.raw_corps_documents[0]]
        self._create_raw_documents_in_db(valid_corps_data)

        # Execute CleanDocuments usecase
        result = self.clean_documents_usecase.execute(DocumentType.CORPS)
        self.assertEqual(result["created"], 1)

        # Verify saved corps can be retrieved by ID
        corps_repository = self.shared_container.corps_repository()
        expected_id = int(self.raw_corps_documents[0]["identifiant"])
        retrieved_corps = corps_repository.find_by_id(expected_id)

        self.assertIsNotNone(retrieved_corps)
        self.assertEqual(retrieved_corps.id, expected_id)
        self.assertIsNotNone(retrieved_corps.label)
        self.assertIsNotNone(retrieved_corps.category)

    @pytest.mark.django_db
    def test_execute_handles_filtering_edge_cases(self):
        """Test various filtering scenarios."""
        # Create documents with different filtering conditions
        valid_corps = self.raw_corps_documents[0].copy()

        # Non-civil servant
        non_civil_servant = self.raw_corps_documents[1].copy()
        non_civil_servant["corpsOuPseudoCorps"]["caracteristiques"]["population"][
            "libellePopulation"
        ] = "Contractuel"

        # MINARM ministry
        minarm_corps = self.raw_corps_documents[2].copy()
        minarm_corps["corpsOuPseudoCorps"]["ministereEtInstitutionDeLaRepublique"][0][
            "libelleMinistere"
        ] = "MINARM"

        self._create_raw_documents_in_db([valid_corps, non_civil_servant, minarm_corps])

        result = self.clean_documents_usecase.execute(DocumentType.CORPS)

        self.assertEqual(result["processed"], 3)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        corps_repository = self.shared_container.corps_repository()

        saved_corps = corps_repository.get_all()
        self.assertEqual(len(saved_corps), 1)

    @pytest.mark.django_db
    def test_corps_repository_find_by_id_nonexistent(self):
        """Test find_by_id returns None for nonexistent Corps."""
        corps_repository = self.shared_container.corps_repository()

        nonexistent_corps = corps_repository.find_by_id(99999)

        self.assertIsNone(nonexistent_corps)

    @pytest.mark.django_db
    def test_corps_repository_get_all_empty(self):
        """Test get_all returns empty list when no Corps exist."""
        corps_repository = self.shared_container.corps_repository()

        all_corps = corps_repository.get_all()

        self.assertEqual(len(all_corps), 0)
        self.assertIsInstance(all_corps, list)

    # CONCOURS Integration Tests

    @pytest.mark.django_db
    def test_execute_handles_empty_concours_documents(self):
        """Test that empty concours document list is handled correctly."""
        result = self.clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["cleaned"], 0)
        self.assertEqual(result["created"], 0)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        saved_concours = ConcoursModel.objects.all()
        self.assertEqual(saved_concours.count(), 0)

    @pytest.mark.django_db
    def test_execute_creates_concours_successfully(self):
        """Test that valid concours documents are processed and saved."""
        valid_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc.get("Statut") == "VALIDE"
            and doc.get("Année de référence", 0) > REFERENCE_YEAR
        ][:2]

        self._create_raw_concours_documents_in_db(valid_concours)

        result = self.clean_documents_usecase.execute(DocumentType.CONCOURS)
        saved_concours = ConcoursModel.objects.all()

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 2)
        self.assertEqual(result["created"], 2)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["errors"], 0)

        self.assertEqual(saved_concours.count(), 2)

    @pytest.mark.django_db
    def test_execute_filters_invalid_concours_status(self):
        """Test that concours with invalid status are filtered out."""
        # Mix valid and invalid status
        valid_concours = [
            doc for doc in self.raw_concours_documents if doc.get("Statut") == "VALIDE"
        ][:1]

        invalid_concours = self.raw_concours_documents[0].copy()
        invalid_concours["Statut"] = "INVALIDE"

        test_data = valid_concours + [invalid_concours]
        self._create_raw_concours_documents_in_db(test_data)

        result = self.clean_documents_usecase.execute(DocumentType.CONCOURS)

        # Only valid status should be processed
        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)

        saved_concours = ConcoursModel.objects.all()
        self.assertEqual(saved_concours.count(), 1)

    @pytest.mark.django_db
    def test_execute_filters_old_year_concours(self):
        """Test that concours with year <= 2024 are filtered out."""
        # Create concours with different years
        new_concours = self.raw_concours_documents[0].copy()
        new_concours["Année de référence"] = 2025
        new_concours["Statut"] = "VALIDE"

        old_concours = self.raw_concours_documents[1].copy()
        old_concours["Année de référence"] = REFERENCE_YEAR
        old_concours["Statut"] = "VALIDE"

        test_data = [new_concours, old_concours]
        self._create_raw_concours_documents_in_db(test_data)

        result = self.clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)

        saved_concours = ConcoursModel.objects.all()
        self.assertEqual(saved_concours.count(), 1)

    @pytest.mark.django_db
    def test_execute_filters_concours_missing_required_fields(self):
        """Test that concours with missing required fields are filtered out."""
        valid_concours = self.raw_concours_documents[0].copy()
        valid_concours["Statut"] = "VALIDE"
        valid_concours["Année de référence"] = 2025

        invalid_concours = self.raw_concours_documents[1].copy()
        invalid_concours["Statut"] = "VALIDE"
        invalid_concours["Année de référence"] = 2025
        invalid_concours["N° NOR"] = None  # Missing required field

        test_data = [valid_concours, invalid_concours]
        self._create_raw_concours_documents_in_db(test_data)

        result = self.clean_documents_usecase.execute(DocumentType.CONCOURS)

        self.assertEqual(result["processed"], 2)
        self.assertEqual(result["cleaned"], 1)
        self.assertEqual(result["created"], 1)

        saved_concours = ConcoursModel.objects.all()
        self.assertEqual(saved_concours.count(), 1)

    @pytest.mark.django_db
    def test_execute_updates_existing_concours(self):
        """Test that existing Concours entities are updated correctly."""
        valid_concours = [
            doc
            for doc in self.raw_concours_documents
            if doc.get("Statut") == "VALIDE"
            and doc.get("Année de référence", 0) > REFERENCE_YEAR
        ][:1]

        self._create_raw_concours_documents_in_db(valid_concours)

        # First execution - create concours
        result1 = self.clean_documents_usecase.execute(DocumentType.CONCOURS)
        self.assertEqual(result1["created"], 1)
        self.assertEqual(result1["updated"], 0)

        # Second execution with same data - should update
        result2 = self.clean_documents_usecase.execute(DocumentType.CONCOURS)
        self.assertEqual(result2["created"], 0)
        self.assertEqual(result2["updated"], 1)

        # Verify only one Concours entity exists
        saved_concours = ConcoursModel.objects.all()
        self.assertEqual(len(saved_concours), 1)

    @pytest.mark.django_db
    def test_concours_repository_find_by_id_nonexistent(self):
        """Test find_by_id returns None for nonexistent Concours."""
        concours_repository = self.shared_container.concours_repository()

        nonexistent_concours = concours_repository.find_by_id(99999)

        self.assertIsNone(nonexistent_concours)

    @pytest.mark.django_db
    def test_concours_repository_get_all_empty(self):
        """Test get_all returns empty list when no Concours exist."""
        concours_repository = self.shared_container.concours_repository()

        all_concours = concours_repository.get_all()

        self.assertEqual(len(all_concours), 0)
        self.assertIsInstance(all_concours, list)
