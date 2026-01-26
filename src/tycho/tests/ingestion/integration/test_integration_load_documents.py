"""Integration tests for LoadDocuments usecase with external adapters."""

import responses
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework.test import APITestCase

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from tests.factories.ingres_factories import IngresCorpsApiResponseFactory

fake = Faker()


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

        # This test ensures that the id of the object stored in the database
        # is managed by the database.
        expected_documents_ids = [
            (i + 1, d.identifiant) for i, d in enumerate(api_response.documents)
        ]
        saved_documents_ids = saved_documents.values_list("id", "external_id")
        assert set(expected_documents_ids) == set(saved_documents_ids)


class TestConcoursUploadView(APITestCase):
    """Integration tests for ConcoursUploadView."""

    def setUp(self):
        """Set up test environment."""
        self.concours_upload_url = "/ingestion/concours/upload/"

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

    def test_no_file_provided(self):
        """Test error when no file is provided."""
        response = self.client.post(self.concours_upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No file provided")

    def test_invalid_file_format(self):
        """Test error when file is not CSV."""
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
