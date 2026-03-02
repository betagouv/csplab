import pytest
from faker import Faker

from domain.entities.document import DocumentType
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.corps_factory import CorpsFactory
from tests.factories.offer_factory import OfferFactory

fake = Faker()

factories_mapper = {
    DocumentType.CORPS: CorpsFactory(),
    DocumentType.CONCOURS: ConcoursFactory(),
    DocumentType.OFFERS: OfferFactory(),
}


@pytest.mark.parametrize(
    "document_type", [DocumentType.CORPS, DocumentType.CONCOURS, DocumentType.OFFERS]
)
def test_vectorize_entity_integration(
    db, ingestion_integration_container, document_type
):
    usecase = ingestion_integration_container.vectorize_documents_usecase()
    documents = factories_mapper[document_type].create_batch(2)

    result = usecase.execute(document_type)

    assert result["processed"] == len(documents)
    assert result["vectorized"] == len(documents)
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == len(documents)

    for vector in saved_vectors:
        assert vector.embedding is not None
        assert len(vector.embedding) > 0
        assert vector.content is not None
        assert vector.metadata is not None


def test_vectorize_empty_list_integration(db, ingestion_integration_container):
    usecase = ingestion_integration_container.vectorize_documents_usecase()

    result = usecase.execute(DocumentType.OFFERS)

    assert result["processed"] == 0
    assert result["vectorized"] == 0
    assert result["errors"] == 0
    assert len(result["error_details"]) == 0

    saved_vectors = VectorizedDocumentModel.objects.all()
    assert saved_vectors.count() == 0


def test_vectorize_limit(db, ingestion_integration_container):
    limit = 2
    OfferFactory.create_batch(limit + 1)
    usecase = ingestion_integration_container.vectorize_documents_usecase()
    result = usecase.execute(DocumentType.OFFERS, limit=limit)

    assert result == {
        "processed": limit,
        "vectorized": limit,
        "errors": 0,
        "error_details": [],
    }
    assert VectorizedDocumentModel.objects.count() == limit
    assert OfferModel.objects.filter(processed_at__isnull=False).count() == limit


# to be tested:
# - [x] empty sources
# - [x] all sources are vectorized : vectorized exits, document is processed not processing
# - [x] limit
# - [ ] partial failures
#   - [ ] get_pending_processing failures
#   - [ ] vectorize failures
#   - [ ] upsert failures
#   - [ ] mark_as_pending failures = rollback on upsert
