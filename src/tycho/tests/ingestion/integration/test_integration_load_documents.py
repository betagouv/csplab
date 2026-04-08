from unittest.mock import patch

import pytest
import responses
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from tests.factories.ingres_factories import IngresCorpsApiResponseFactory

fake = Faker()


class TestIntegrationCorpsLoadDocumentsUseCase:
    @responses.activate
    def test_execute_returns_zero_when_no_documents(
        self, db, documents_integration_usecase, test_app_config
    ):
        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint with empty response
        responses.add(
            responses.GET,
            f"{test_app_config.ingres_base_url}/CORPS",
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
        self, db, documents_integration_usecase, test_app_config
    ):
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        responses.add(
            responses.POST,
            f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status=200,
            content_type="application/json",
        )

        # Mock INGRES API endpoint
        responses.add(
            responses.GET,
            f"{test_app_config.ingres_base_url}/CORPS",
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
    def setUp(self):
        self.concours_upload_url = "/ingestion/concours/upload/"
        # Create a test user for authenticated tests
        self.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=fake.password()
        )

    def _get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def _authenticate_client(self, user):
        token = self._get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def _create_valid_csv_content(self):
        return (
            "N° NOR;Ministère;Catégorie;Corps;"
            "Grade;Année de référence;Nb postes total\n"
            "INTB2400001C;Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
            "INTB2400002C;Ministère de l'Intérieur;B;Secrétaire;Secrétaire;2024;5\n"
        )

    def _create_invalid_csv_content(self):
        return (
            "N° NOR;Ministère;Catégorie;Corps;Grade;"
            "Année de référence;Nb postes total\n"
            ";Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"  # Missing NOR
            "INTB2400002C;;B;Secrétaire;Secrétaire;2024;5\n"  # Missing Ministère
        )

    def _create_csv_file(self, content, filename="test.csv"):
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    def test_unauthenticated_access_returns_401(self):
        # Ensure client is not authenticated
        self.client.logout()

        valid_csv = self._create_csv_file(self._create_valid_csv_content())
        response = self.client.post(
            self.concours_upload_url, {"file": valid_csv}, format="multipart"
        )

        self.assertEqual(response.status_code, 401)

    def test_no_file_provided(self):
        self._authenticate_client(self.user)
        response = self.client.post(self.concours_upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No file provided")

    def test_invalid_file_format(self):
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


@pytest.fixture(name="api_client")
def api_client_fixture():
    return APIClient()


@pytest.fixture(name="user")
def user_fixture(db):
    return User.objects.create_user(
        username=fake.name(), email=fake.email(), password=fake.password()
    )


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(api_client, user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


class TestHueyHealthView:
    url = reverse("health-huey")

    def test_success_response(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_access(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_redis_unavailable(self, authenticated_client):
        with patch("huey.contrib.djhuey.HUEY.storage.conn.ping") as mocked_ping:
            mocked_ping.side_effect = Exception("Redis connection refused")
            response = authenticated_client.get(self.url)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data == {"status": "Huey health check failed"}
