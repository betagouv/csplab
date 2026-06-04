import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status


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
