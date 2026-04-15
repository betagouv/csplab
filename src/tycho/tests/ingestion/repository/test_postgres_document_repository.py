from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from faker import Faker

from domain.entities.document import Document, DocumentType
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.repositories.ingestion.postgres_document_repository import (
    PostgresDocumentRepository,
)
from tests.factories.raw_document_factory import RawDocumentFactory

fake = Faker()

NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture
def repository():
    return PostgresDocumentRepository()


@pytest.fixture(autouse=True)
def clean_database(db):
    # Clean up before test runs
    RawDocument.objects.all().delete()
    yield
    # Clean up after test runs (optional, but good practice)
    RawDocument.objects.all().delete()


class TestFindByType:
    @pytest.mark.parametrize(
        "start,batch_size",
        [
            pytest.param(-1, 1, id="negative start"),
            pytest.param(0, 0, id="zero batch_size"),
            pytest.param(0, -1, id="negative batch_size"),
        ],
    )
    def test_invalid_parameters(self, db, repository, start, batch_size):
        with pytest.raises(ValueError, match="Invalid start or batch_size values"):
            repository.find_by_type(
                DocumentType.OFFERS, start=start, batch_size=batch_size
            )

    def test_empty_results(self, db, repository):
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


class TestFindByExternalIds:
    def test_handle_empty_results(self, db, repository):
        documents = repository.find_by_external_ids(
            document_type=DocumentType.OFFERS, documents=[]
        )
        assert documents == []

    def test_ignore_other_document_type(self, db, repository):
        external_id = "uuid-1"
        raw_document = RawDocumentFactory.create(
            document_type=DocumentType.OFFERS, external_id=external_id
        )
        RawDocumentFactory.create(
            document_type=DocumentType.CORPS, external_id=external_id
        )
        RawDocumentFactory.create(
            document_type=DocumentType.CONCOURS, external_id=external_id
        )

        documents = repository.find_by_external_ids(
            document_type=DocumentType.OFFERS, documents=[raw_document.to_entity()]
        )

        assert len(documents) == 1
        document = documents[0]
        assert isinstance(document, Document)
        assert document.external_id == external_id
        assert document.type == DocumentType.OFFERS

    def test_find_correct_external_ids(self, db, repository):
        raw_documents_models = [
            RawDocumentFactory.create(
                document_type=DocumentType.OFFERS, external_id=f"uuid-{i}"
            )
            for i in range(3)
        ]
        raw_documents = [
            raw_document.to_entity() for raw_document in raw_documents_models
        ]

        documents = repository.find_by_external_ids(
            document_type=DocumentType.OFFERS, documents=raw_documents[:2]
        )

        assert {d.external_id for d in documents} == {"uuid-0", "uuid-1"}


class TestUpsertBatch:
    def test_datetime_on_upsert(self, db, repository):
        raw_doc = RawDocumentFactory.create()
        raw_doc_to_update = RawDocumentFactory.create()
        new_raw_doc = RawDocumentFactory.create(save_in_db=False)

        documents = [
            RawDocument.to_entity(raw_doc_to_update),
            RawDocument.to_entity(new_raw_doc),
        ]

        timestamps = {
            raw_doc: (raw_doc.created_at, raw_doc.updated_at),
            raw_doc_to_update: (
                raw_doc_to_update.created_at,
                raw_doc_to_update.updated_at,
            ),
        }

        assert not RawDocument.objects.filter(
            external_id=new_raw_doc.external_id
        ).exists()

        repository.upsert_batch(documents, DocumentType.OFFERS)

        created_at, updated_at = timestamps[raw_doc]
        raw_doc.refresh_from_db()
        assert raw_doc.created_at == created_at
        assert raw_doc.updated_at == updated_at

        created_at, updated_at = timestamps[raw_doc_to_update]
        raw_doc_to_update.refresh_from_db()
        assert raw_doc_to_update.created_at == created_at
        assert raw_doc_to_update.updated_at > updated_at

        assert RawDocument.objects.filter(external_id=new_raw_doc.external_id).exists()


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        RawDocumentFactory.create(document_type=DocumentType.CORPS)
        RawDocumentFactory.create(document_type=DocumentType.CONCOURS)
        RawDocumentFactory.create(processing=True)
        RawDocumentFactory.create(processed_at=NOW, updated_at=DAY_AGO)

        assert (
            repository.get_pending_processing(document_type=DocumentType.OFFERS) == []
        )

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = RawDocumentFactory.create()
        updated_after_processed = RawDocumentFactory.create(
            processed_at=DAY_AGO, updated_at=NOW
        )

        entities = repository.get_pending_processing(document_type=DocumentType.OFFERS)
        assert {e.id for e in entities} == {
            never_processed.id,
            updated_after_processed.id,
        }

        for entity in entities:
            assert isinstance(entity, Document)
            assert entity.processing

    def test_limit(self, db, repository):
        RawDocumentFactory.create_batch(2)

        entities = repository.get_pending_processing(
            document_type=DocumentType.OFFERS, limit=1
        )
        assert len(entities) == 1
        assert RawDocument.objects.filter(processing=True).count() == 1
        assert RawDocument.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    raw_documents = [
        RawDocumentFactory.create(processing=True).to_entity(),
        RawDocumentFactory.create(processing=False).to_entity(),
    ]
    undesired_raw_document = RawDocumentFactory.create(processing=True).to_entity()

    count = repository.mark_as_processed(raw_documents)
    assert count == len(raw_documents)

    model_objects = RawDocument.objects.filter(
        processing=False, processed_at__isnull=False
    )
    assert set(model_objects.values_list("id", flat=True)) == {
        raw_document.id for raw_document in raw_documents
    }

    undesired_model_objects = RawDocument.objects.get(
        processing=True, processed_at__isnull=True
    )
    assert undesired_model_objects.id == undesired_raw_document.id


def test_mark_as_pending(db, repository):
    raw_documents = [
        RawDocumentFactory.create(processing=True).to_entity(),
        RawDocumentFactory.create(processing=False).to_entity(),
    ]
    undesired_raw_document = RawDocumentFactory.create(processing=True).to_entity()

    count = repository.mark_as_pending(raw_documents)
    assert count == len(raw_documents)

    model_objects = RawDocument.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        raw_document.id for raw_document in raw_documents
    }

    undesired_model_objects = RawDocument.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_raw_document.id
