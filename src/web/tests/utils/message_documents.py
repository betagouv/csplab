import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

PDF_BYTES = b"%PDF-1.4 contenu"
PNG_BYTES = b"\x89PNG\r\n\x1a\n contenu"
JPEG_BYTES = b"\xff\xd8\xff contenu"


def pdf(name="document.pdf", content=PDF_BYTES):
    return SimpleUploadedFile(name, content, content_type="application/pdf")


def valid_documents():
    documents = [
        pdf("cv.pdf"),
        pdf("lettre.pdf"),
        pdf("diplome.pdf"),
        SimpleUploadedFile("photo.png", PNG_BYTES, content_type="image/png"),
        SimpleUploadedFile("scan.jpg", JPEG_BYTES, content_type="image/jpeg"),
    ]
    assert len(documents) == settings.MESSAGE_MAX_DOCUMENTS
    return documents


def _too_many_documents():
    return [pdf(f"{i}.pdf") for i in range(settings.MESSAGE_MAX_DOCUMENTS + 1)]


def _document_too_large():
    max_size = settings.MESSAGE_DOCUMENT_MAX_SIZE_MB * 1024 * 1024
    return [pdf(content=PDF_BYTES.ljust(max_size + 1))]


def _unsupported_type():
    return [SimpleUploadedFile("notes.txt", b"texte", content_type="text/plain")]


def _spoofed_content_type():
    return [SimpleUploadedFile("faux.png", PDF_BYTES, content_type="image/png")]


# Construits paresseusement pour ne pas allouer le fichier trop volumineux à l'import
INVALID_DOCUMENTS = [
    pytest.param(_too_many_documents, id="too_many_documents"),
    pytest.param(_document_too_large, id="document_too_large"),
    pytest.param(_unsupported_type, id="unsupported_type"),
    pytest.param(_spoofed_content_type, id="spoofed_content_type"),
]
