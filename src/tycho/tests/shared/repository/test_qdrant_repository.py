import pytest
from django.conf import settings

from domain.entities.document import DocumentType
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory
from tests.fixtures.shared_fixtures import create_shared_qdrant_repository

DELETED_DOCUMENTS_COUNT = 2


@pytest.mark.django_db
def test_qdrant_repository(db):
    qdrant_repo = create_shared_qdrant_repository()

    vectorized_documents = VectorizedDocumentFactory.create_batch(
        size=3,
        document_type=DocumentType.OFFERS,
        metadata={"category": "test", "source": "integration_test"},
    )

    doc1_id = vectorized_documents[0].entity_id
    doc2_id = vectorized_documents[1].entity_id
    doc3_id = vectorized_documents[2].entity_id

    qdrant_repo.upsert_batch(vectorized_documents, DocumentType.OFFERS)

    test_embedding = [0.1] * settings.EMBEDDING_DIMENSION

    ids_to_delete = [doc1_id, doc2_id]
    delete_result = qdrant_repo.delete_vectorized_documents(ids_to_delete)

    assert "deleted" in delete_result
    assert "errors" in delete_result
    assert isinstance(delete_result["deleted"], int)
    assert isinstance(delete_result["errors"], list)

    assert delete_result["deleted"] == DELETED_DOCUMENTS_COUNT
    assert len(delete_result["errors"]) == 0

    search_results_after_delete = qdrant_repo.semantic_search(
        query_embedding=test_embedding,
        limit=10,
        filters={"document_type": DocumentType.OFFERS.value},
    )

    found_ids_after_delete = {
        result.document.entity_id for result in search_results_after_delete
    }

    assert doc1_id not in found_ids_after_delete
    assert doc2_id not in found_ids_after_delete
    assert doc3_id in found_ids_after_delete
