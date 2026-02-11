"""Integration tests for CV upload view."""

from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from presentation.candidate.forms.cv_flow import CV_MAX_SIZE_BYTES
from tests.utils.form_test_utils import assert_form_error_code
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


def test_cv_upload_page_loads_correctly(client, db):
    """GET returns 200 with correct template, form, CSRF, important UI classes."""
    response = client.get(reverse("candidate:cv_upload"))

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_upload.html")
    assertContains(response, 'id="cv-upload-form"')
    assertContains(response, 'enctype="multipart/form-data"')
    assertContains(response, "csrfmiddlewaretoken")
    assertContains(response, "csplab-dropzone")
    assertContains(response, "no-js-only")


@pytest.mark.parametrize("filename", ["cv.pdf", "CV.PDF"])
@patch("presentation.candidate.views.cv_flow.create_candidate_container")
def test_cv_upload_valid_pdf_redirects_to_results(mock_container, client, db, filename):
    """Valid PDF uploads redirect to cv_results view."""
    # Mock the usecases
    mock_uuid = str(uuid4())
    mock_initialize_usecase = (
        mock_container.return_value.initialize_cv_metadata_usecase.return_value
    )
    mock_initialize_usecase.execute.return_value = mock_uuid

    # Mock async usecase to return a coroutine
    async def mock_async_execute(cv_uuid, cv_content):
        return None

    mock_process_usecase = (
        mock_container.return_value.process_uploaded_cv_usecase.return_value
    )
    mock_process_usecase.execute = mock_async_execute

    pdf = SimpleUploadedFile(filename, create_minimal_valid_pdf(), "application/pdf")
    response = client.post(
        reverse("candidate:cv_upload"), {"cv_file": pdf}, follow=True
    )

    # Check redirect to cv_results with correct URL pattern
    assert response.redirect_chain[-1][0] == f"/candidate/cv/{mock_uuid}/results/"


def test_cv_upload_empty_submission_shows_error(client, db):
    """POST without file shows required field error."""
    response = client.post(reverse("candidate:cv_upload"), {})
    assert response.status_code == HTTPStatus.OK
    assert_form_error_code(response, "cv_file", "required")
    assertContains(response, "Ce champ est obligatoire")


@pytest.mark.parametrize(
    "filename,content,content_type,expected_error_code,expected_message_fragment",
    [
        (
            "large.pdf",
            lambda: create_minimal_valid_pdf() + b"x" * (CV_MAX_SIZE_BYTES + 1000),
            "application/pdf",
            "file_too_large",
            "Le fichier dépasse la taille maximale",
        ),
        (
            "cv.pdf",
            lambda: create_minimal_valid_pdf(),
            "text/plain",
            "invalid_content_type",
            "Format non supporté. Seul le format PDF est accepté.",
        ),
        (
            "cv.doc",
            lambda: create_minimal_valid_pdf(),
            "application/pdf",
            "invalid_extension",
            "Extension non supportée. Seul le format PDF est accepté.",
        ),
        (
            "fake.pdf",
            lambda: b"Not a PDF",
            "application/pdf",
            "invalid_pdf_signature",
            "Le fichier n'est pas un PDF valide.",
        ),
    ],
)
def test_cv_upload_invalid_files_are_rejected(
    client,
    db,
    filename,
    content,
    content_type,
    expected_error_code,
    expected_message_fragment,
):
    """Invalid files are rejected with appropriate error codes and messages."""
    file = SimpleUploadedFile(filename, content(), content_type)
    response = client.post(reverse("candidate:cv_upload"), {"cv_file": file})
    assert response.status_code == HTTPStatus.OK
    assert_form_error_code(response, "cv_file", expected_error_code)
    assertContains(response, expected_message_fragment)
