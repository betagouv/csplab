"""Integration tests for CV upload view."""

from http import HTTPStatus

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from presentation.candidate.forms.cv_flow import CV_MAX_SIZE_BYTES
from tests.utils.pdf_test_utils import create_minimal_valid_pdf


@pytest.mark.django_db
def test_cv_upload_page_loads_with_correct_template(client):
    """GET request returns 200 and uses cv_upload.html template."""
    response = client.get(reverse("candidate:cv_upload"))
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_upload.html")


@pytest.mark.django_db
def test_cv_upload_page_contains_upload_form_and_both_uis(client):
    """Page contains the form with both JS dropzone and no-JS fallback."""
    response = client.get(reverse("candidate:cv_upload"))
    assertContains(response, 'id="cv-upload-form"')
    assertContains(response, 'enctype="multipart/form-data"')
    assertContains(response, "csplab-dropzone")
    assertContains(response, "no-js-only")


@pytest.mark.django_db
def test_cv_upload_form_has_csrf_protection(client):
    """Form includes CSRF token for security."""
    response = client.get(reverse("candidate:cv_upload"))
    assertContains(response, "csrfmiddlewaretoken")


@pytest.mark.django_db
def test_cv_upload_file_input_has_accessible_label(client):
    """File input has visible label for screen readers."""
    response = client.get(reverse("candidate:cv_upload"))
    assertContains(response, "Votre CV")


@pytest.mark.django_db
def test_cv_upload_valid_pdf_upload_shows_success_message(client):
    """Valid PDF upload redirects and shows success message."""
    pdf = SimpleUploadedFile("cv.pdf", create_minimal_valid_pdf(), "application/pdf")
    response = client.post(
        reverse("candidate:cv_upload"), {"cv_file": pdf}, follow=True
    )
    assertContains(response, "validé avec succès")


@pytest.mark.django_db
def test_cv_upload_uppercase_extension_is_accepted(client):
    """PDF with uppercase extension (.PDF) passes validation."""
    pdf = SimpleUploadedFile("CV.PDF", create_minimal_valid_pdf(), "application/pdf")
    response = client.post(
        reverse("candidate:cv_upload"), {"cv_file": pdf}, follow=True
    )
    assertContains(response, "validé avec succès")


@pytest.mark.django_db
def test_cv_upload_empty_submission_shows_error(client):
    """POST without file shows required field error."""
    response = client.post(reverse("candidate:cv_upload"), {})
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Ce champ est obligatoire")


@pytest.mark.django_db
def test_cv_upload_oversized_file_is_rejected(client):
    """File exceeding 5MB is rejected with size error message."""
    oversized = SimpleUploadedFile(
        "large.pdf",
        create_minimal_valid_pdf() + b"x" * (CV_MAX_SIZE_BYTES + 1000),
        "application/pdf",
    )
    response = client.post(reverse("candidate:cv_upload"), {"cv_file": oversized})
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "taille maximale")


@pytest.mark.django_db
def test_cv_upload_wrong_content_type_is_rejected(client):
    """Non-PDF content type (text/plain) is rejected."""
    txt = SimpleUploadedFile("cv.txt", b"Plain text content", "text/plain")
    response = client.post(reverse("candidate:cv_upload"), {"cv_file": txt})
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "PDF")


@pytest.mark.django_db
def test_cv_upload_wrong_extension_is_rejected(client):
    """File with .doc extension is rejected even with valid PDF content."""
    doc = SimpleUploadedFile("cv.doc", create_minimal_valid_pdf(), "application/pdf")
    response = client.post(reverse("candidate:cv_upload"), {"cv_file": doc})
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Extension")


@pytest.mark.django_db
def test_cv_upload_fake_pdf_without_valid_structure_is_rejected(client):
    """File with .pdf extension but invalid PDF structure is rejected."""
    fake = SimpleUploadedFile("fake.pdf", b"Not a PDF", "application/pdf")
    response = client.post(reverse("candidate:cv_upload"), {"cv_file": fake})
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "PDF valide")
