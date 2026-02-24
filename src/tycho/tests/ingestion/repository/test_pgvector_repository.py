import copy
import random
from uuid import uuid4

import numpy as np
import pytest
from django.db import DatabaseError, IntegrityError
from faker import Faker

from domain.entities.document import DocumentType
from infrastructure.django_apps.shared.models.vectorized_document import (
    VectorizedDocumentModel,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.pgvector_repository import (
    PgVectorRepository,
)
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory

fake = Faker()


@pytest.fixture(name="repository")
def repository_fixture():
    return PgVectorRepository(LoggerService())


@pytest.mark.parametrize("document_type", list(DocumentType))
def test_entity_id_and_document_type_combination_is_unique(db, document_type):
    entity_id = uuid4()
    VectorizedDocumentFactory.create(entity_id=entity_id, document_type=document_type)

    with pytest.raises(IntegrityError):
        VectorizedDocumentFactory.create(
            entity_id=entity_id, document_type=document_type
        )


class TestUpsertBatch:
    @pytest.mark.parametrize("document_type", list(DocumentType))
    def test_upsert_logic(self, db, repository, document_type):
        vectorized_documents = VectorizedDocumentFactory.create_batch(
            2, document_type=document_type
        )
        vectorized_doc_to_insert = vectorized_documents[0].to_entity()
        vectorized_doc_to_insert.id = uuid4()
        vectorized_doc_to_insert.entity_id = uuid4()

        content = fake.paragraph()
        embedding = [random.random() for i in range(3072)]
        metadata = {"property": fake.name()}
        vectorized_doc_to_update = vectorized_documents[0].to_entity()
        vectorized_doc_to_update.content = content
        vectorized_doc_to_update.embedding = embedding
        vectorized_doc_to_update.metadata = metadata

        vectorized_doc_unchanged = vectorized_documents[1].to_entity()

        results = repository.upsert_batch(
            [
                vectorized_doc_to_insert,
                vectorized_doc_to_update,
                vectorized_doc_unchanged,
            ],
            document_type,
        )

        assert results == {"created": 1, "updated": 2, "errors": []}

        for entity in (
            vectorized_doc_to_insert,
            vectorized_doc_to_update,
            vectorized_doc_unchanged,
        ):
            model_obj = VectorizedDocumentModel.objects.get(id=entity.id)
            for field in (
                "id",
                "entity_id",
                "content",
                "metadata",
            ):
                assert getattr(model_obj, field) == getattr(entity, field)

            assert np.array_equal(
                np.array(entity.embedding, dtype=np.float32), model_obj.embedding
            )

    def test_num_queries(self, db, repository):
        vectorized_documents = VectorizedDocumentFactory.create_batch(10)
        entities = []
        for model_obj in vectorized_documents:
            entity = model_obj.to_entity()
            entities.append(entity)

            new_entity = copy.deepcopy(entity)
            new_entity.id = uuid4()
            new_entity.entity_id = uuid4()
            entities.append(new_entity)

        results = repository.upsert_batch(entities, DocumentType.OFFERS)

        assert results == {"created": 10, "updated": 10, "errors": []}

    def test_upsert_with_errors(self, db, repository):
        vectorized_document = VectorizedDocumentFactory.create().to_entity()
        vectorized_document.entity_id = "not an uuid"

        results = repository.upsert_batch([vectorized_document], DocumentType.OFFERS)
        error = results["errors"][0]

        assert "Database error during bulk upsert" in error["error"]
        assert isinstance(error["exception"], DatabaseError)
