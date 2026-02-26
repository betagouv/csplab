from uuid import uuid4

import pytest
from django.db import IntegrityError

from domain.entities.document import DocumentType
from tests.factories.vectorized_document_factory import VectorizedDocumentFactory


@pytest.mark.parametrize("document_type", list(DocumentType))
def test_entity_id_and_document_type_combination_is_unique(db, document_type):
    entity_id = uuid4()
    VectorizedDocumentFactory.create(entity_id=entity_id, document_type=document_type)

    with pytest.raises(IntegrityError):
        VectorizedDocumentFactory.create(
            entity_id=entity_id, document_type=document_type
        )
