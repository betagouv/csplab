from uuid import uuid4

import pytest

from application.ingestion.errors.application_errors_ingestion import (
    SourceIntrouvable,
)
from application.ingestion.services.get_source import get_source
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)


def test_returns_the_source(db):
    source = SourceDjangoFactory()

    assert get_source(source.source_id) == source


def test_refuses_an_unknown_source(db):
    with pytest.raises(SourceIntrouvable):
        get_source(uuid4())
