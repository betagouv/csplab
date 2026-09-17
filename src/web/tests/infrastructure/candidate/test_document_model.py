from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)


def test_document_roundtrips_through_storage(db):
    document = DocumentDjangoFactory()

    assert document.fichier.read() == b"%PDF-1.4\n%test"


def test_document_upload_to_key_shape(db):
    document = DocumentDjangoFactory()

    assert document.fichier.name == (
        f"candidatures/{document.candidature_id}/documents/{document.id}"
    )
