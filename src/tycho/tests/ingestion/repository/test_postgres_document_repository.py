"""Integration tests for PostgresDocumentRepository (with real database)."""

import pytest

from domain.entities.document import DocumentType
from infrastructure.repositories.ingestion.postgres_document_repository import (
    PostgresDocumentRepository,
)
from tests.factories.raw_document_factory import RawDocumentFactory


@pytest.fixture
def repository():
    """Create a PostgresDocumentRepository instance."""
    return PostgresDocumentRepository()


class TestFindByType:
    """Test find_by_type method with real database."""

    @pytest.mark.parametrize(
        "start,batch_size",
        [
            pytest.param(-1, 1, id="negative start"),
            pytest.param(0, 0, id="zero batch_size"),
            pytest.param(0, -1, id="negative batch_size"),
        ],
    )
    def test_invalid_parameters(self, db, repository, start, batch_size):
        """Test that invalid parameters raise ValueError."""
        with pytest.raises(ValueError, match="Invalid start or batch_size values"):
            repository.find_by_type(
                DocumentType.OFFERS, start=start, batch_size=batch_size
            )

    def test_empty_results(self, db, repository):
        """Test fetching when no documents exist."""
        documents, has_more = repository.find_by_type(
            DocumentType.OFFERS, start=0, batch_size=10
        )

        assert documents == []
        assert has_more is False

    @pytest.mark.parametrize(
        "start,fetched_docs,expected_has_more",
        [
            pytest.param(0, 2, True, id="first page"),
            pytest.param(1, 2, True, id="second page"),
            pytest.param(2, 1, False, id="last page"),
            pytest.param(3, 0, False, id="out of range page"),
        ],
    )
    def test_offsetting(self, db, repository, start, fetched_docs, expected_has_more):
        """Test has_more flag when more documents exist beyond current batch."""
        total_docs = 5
        batch_size = 2
        document_type = DocumentType.OFFERS
        RawDocumentFactory.create_batch(total_docs, document_type)

        documents, has_more = repository.find_by_type(
            document_type, start=start, batch_size=batch_size
        )

        assert len(documents) == fetched_docs
        assert has_more is expected_has_more

    def test_filtering_with_mixed_document_type(self, db, repository):
        """Test that fetch_by_type correctly filters by document type."""
        nb_doc_per_type = batch_size = 2
        for document_type in DocumentType:
            RawDocumentFactory.create_batch(
                nb_doc_per_type, document_type=document_type
            )

        for document_type in DocumentType:
            docs, has_more = repository.find_by_type(
                document_type, start=0, batch_size=batch_size
            )
            assert len(docs) == nb_doc_per_type
            assert all(doc.type == document_type for doc in docs)
            assert has_more is False

    def test_fetch_by_type_returns_documents_in_id_order(self, db, repository):
        """Test that documents are returned in ID order (insertion order)."""
        document_type = DocumentType.OFFERS
        expected_document_count = 2

        # Create documents with specific external_ids in sequence
        RawDocumentFactory.create(document_type=document_type, external_id="uuid-1")
        RawDocumentFactory.create(document_type=document_type, external_id="uuid-2")

        documents, _ = repository.find_by_type(document_type, start=0, batch_size=10)

        # Should be ordered by database ID (insertion order)
        assert len(documents) == expected_document_count
        assert documents[0].external_id == "uuid-1"
        assert documents[1].external_id == "uuid-2"
