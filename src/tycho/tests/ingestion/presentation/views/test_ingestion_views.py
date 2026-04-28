from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker()


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
    url = reverse("api:health_huey")

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


@pytest.fixture(name="valid_csv_content")
def valid_csv_content_fixture():
    return (
        "N° NOR;Ministère;Catégorie;Corps;"
        "Grade;Année de référence;Nb postes total\n"
        "INTB2400001C;Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
        "INTB2400002C;Ministère de l'Intérieur;B;Secrétaire;Secrétaire;2024;5\n"
    )


@pytest.fixture(name="invalid_csv_content")
def invalid_csv_content_fixture():
    return (
        "N° NOR;Ministère;Catégorie;Corps;Grade;"
        "Année de référence;Nb postes total\n"
        ";Ministère de l'Intérieur;A;Attaché;Attaché;2024;10\n"
        "INTB2400002C;;B;Secrétaire;Secrétaire;2024;5\n"
    )


def make_csv_file(content, filename="test.csv"):
    return SimpleUploadedFile(
        filename, content.encode("utf-8"), content_type="text/csv"
    )


class TestConcoursUploadView:
    url = reverse("ingestion:concours_upload")

    def test_unauthenticated_access(self, api_client, valid_csv_content):
        response = api_client.post(
            self.url, {"file": make_csv_file(valid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_no_file_provided(self, authenticated_client):
        response = authenticated_client.post(self.url, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No file provided"

    def test_invalid_file_format(self, authenticated_client):
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )
        response = authenticated_client.post(
            self.url, {"file": txt_file}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "File must be a CSV"

    def test_validation_errors(self, authenticated_client, invalid_csv_content):
        response = authenticated_client.post(
            self.url, {"file": make_csv_file(invalid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No valid rows found"
        assert "validation_errors" in response.data
        assert len(response.data["validation_errors"]) == 2  # noqa

    def test_success_response(self, db, authenticated_client, valid_csv_content):
        response = authenticated_client.post(
            self.url, {"file": make_csv_file(valid_csv_content)}, format="multipart"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "success"
        assert response.data["total_rows"] == 2  # noqa
        assert response.data["valid_rows"] == 2  # noqa
        assert response.data["invalid_rows"] == 0
        assert (
            "Successfully processed 2 valid concours records"
            in response.data["message"]
        )
