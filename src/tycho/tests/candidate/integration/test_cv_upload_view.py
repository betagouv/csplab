"""Integration tests for CV upload view."""

from http import HTTPStatus

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
def test_cv_upload_valid_pdf_shows_success_message(client, db, filename):
    """Valid PDF uploads redirect and show success message."""
    pdf = SimpleUploadedFile(filename, create_minimal_valid_pdf(), "application/pdf")
    response = client.post(
        reverse("candidate:cv_upload"), {"cv_file": pdf}, follow=True
    )
    assertContains(response, "validé avec succès")


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
def test_cv_upload_invalid_files_are_rejected(  # noqa: PLR0913
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
