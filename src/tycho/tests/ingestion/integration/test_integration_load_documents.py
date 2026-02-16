"""Integration tests for LoadDocuments usecase with external adapters."""

from datetime import datetime

import pytest
import responses
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from tests.external_gateways.utils import cached_token, offers_response
from tests.factories.ingres_factories import IngresCorpsApiResponseFactory

fake = Faker()


def create_offer_documents(container, document_type, raw_offers):
    """Insert RawDocument from json offers."""
    documents = []
    for raw_data in raw_offers["data"]:
        versant_dict = raw_data.get("salaryRange", None)
        versant = versant_dict.get("clientCode", "UNK") if versant_dict else "UNK"
        external_id = f"{versant}-{raw_data['reference']}"
        documents.append(
            Document(
                external_id=external_id,
                raw_data=raw_data,
                type=document_type,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
    repository = container.document_persister()
    repository.upsert_batch(documents, document_type)


class TestIntegrationOfferLoadDocumentUseCase:
    """Test LoadDocuments use case for Offer docs."""

    @pytest.mark.parametrize("count", [0, 2])
    def test_execute_returns_correct_counts(
        self, db, httpx_mock, ingestion_integration_container, count
    ):
        """Test execute returns correct count based on parameter."""
        usecase = ingestion_integration_container.load_documents_usecase()
        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=offers_response(count=count),
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = usecase.execute(input_data)
        assert result["created"] == count
        assert result["updated"] == 0

    def test_execute_returns_correct_counts_with_iterations(
        self, db, httpx_mock, ingestion_integration_container
    ):
        """Test execute returns correct count based on parameter."""
        document_type = DocumentType.OFFERS
        count_existing_offers = 4
        count_new_offers = 3
        usecase = ingestion_integration_container.load_documents_usecase()

        raw_offers = offers_response(count=count_existing_offers, has_more=True)
        create_offer_documents(
            ingestion_integration_container, document_type, raw_offers
        )
        new_raw_offers = offers_response(count=count_new_offers, has_more=False)

        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=raw_offers,
            status_code=200,
        )

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=2",
            json=new_raw_offers,
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = usecase.execute(input_data)
        assert result["created"] == count_new_offers
        assert result["updated"] == count_existing_offers

    @pytest.mark.httpx_mock(can_send_already_matched_responses=True)
    def test_execute_returns_zero_when_api_fails(
        self, db, httpx_mock, ingestion_integration_container
    ):
        """Test execute returns 0 when API call fails."""
        usecase = ingestion_integration_container.load_documents_usecase()
        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            status_code=500,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    @pytest.mark.parametrize(
        "data", ["not_a_list", ["not_a_list_of_dict"], [{"missing_reference_key": 1}]]
    )
    def test_execute_returns_zero_when_api_response_is_malformed(
        self, db, httpx_mock, ingestion_integration_container, data
    ):
        """Test execute returns 0 when API response is malformed."""
        usecase = ingestion_integration_container.load_documents_usecase()

        raw_offers = offers_response()
        raw_offers["data"] = data

        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        httpx_mock.add_response(
            method="GET",
            url=f"{client.base_url}/api/v2/offersummaries?count=1000&start=1",
            json=raw_offers,
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )
        result = usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0


class TestIntegrationCorpsLoadDocumentsUseCase:
    """Test LoadDocuments use case for Corps docs."""

    @responses.activate
    def test_execute_returns_zero_when_no_documents(
        self, db, documents_integration_usecase, piste_gateway_config
    ):
        """Test execute returns 0 when repository is empty."""
        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": []},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_integration_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    @responses.activate
    def test_execute_returns_correct_count_with_documents(
        self, db, documents_integration_usecase, piste_gateway_config
    ):
        """Test execute returns correct count when documents exist with mocked API."""
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{piste_gateway_config.piste.oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{piste_gateway_config.piste.ingres_base_url}/CORPS",
            json={"items": api_data},
            status=200,
            content_type="application/json",
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = documents_integration_usecase.execute(input_data)
        assert result["created"] == len(api_data)
        assert result["updated"] == 0

        # Verify documents are persisted in database
        saved_documents = RawDocument.objects.filter(
            document_type=DocumentType.CORPS.value
        )
        assert saved_documents.count() == len(api_data)


class TestConcoursUploadView(APITestCase):
    """Integration tests for ConcoursUploadView."""

    def setUp(self):
        """Set up test environment."""
        self.concours_upload_url = "/ingestion/concours/upload/"
        # Create a test user for authenticated tests
        self.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=fake.password()
        )

    def _get_jwt_token(self, user):
        """Generate JWT token for the given user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def _authenticate_client(self, user):
        """Authenticate the test client with JWT token."""
        token = self._get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def _create_valid_csv_content(self):
        """Create valid CSV content for testing."""
        return (
            "N° NOR;Ministère;Catégorie;Corps;"
            "Grade;Année de référence;Nb postes total\n"
            "INTB2400001C;Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
            "INTB2400002C;Ministère de l'Intérieur;B;Secrétaire;Secrétaire;2024;5\n"
        )

    def _create_invalid_csv_content(self):
        """Create invalid CSV content for testing."""
        return (
            "N° NOR;Ministère;Catégorie;Corps;Grade;"
            "Année de référence;Nb postes total\n"
            ";Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"  # Missing NOR
            "INTB2400002C;;B;Secrétaire;Secrétaire;2024;5\n"  # Missing Ministère
        )

    def _create_csv_file(self, content, filename="test.csv"):
        """Create a temporary CSV file for testing."""
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    def test_unauthenticated_access_returns_401(self):
        """Test that unauthenticated requests return 401."""
        # Ensure client is not authenticated
        self.client.logout()

        valid_csv = self._create_csv_file(self._create_valid_csv_content())
        response = self.client.post(
            self.concours_upload_url, {"file": valid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 401)

    def test_no_file_provided(self):
        """Test error when no file is provided."""
        self._authenticate_client(self.user)
        response = self.client.post(self.concours_upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No file provided")

    def test_invalid_file_format(self):
        """Test error when file is not CSV."""
        self._authenticate_client(self.user)
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )

        response = self.client.post(
            self.concours_upload_url, {"file": txt_file}, format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "File must be a CSV")

    def test_validation_errors(self):
        """Test handling of validation errors in CSV data."""
        self._authenticate_client(self.user)
        invalid_csv = self._create_csv_file(self._create_invalid_csv_content())

        response = self.client.post(
            self.concours_upload_url, {"file": invalid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No valid rows found")
        self.assertIn("validation_errors", response.data)
        self.assertEqual(len(response.data["validation_errors"]), 2)

    def test_success_response(self):
        """Test successful CSV upload and processing."""
        self._authenticate_client(self.user)
        valid_csv = self._create_csv_file(self._create_valid_csv_content())

        response = self.client.post(
            self.concours_upload_url, {"file": valid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["total_rows"], 2)
        self.assertEqual(response.data["valid_rows"], 2)
        self.assertEqual(response.data["invalid_rows"], 0)
        self.assertIn(
            "Successfully processed 2 valid concours records", response.data["message"]
        )
