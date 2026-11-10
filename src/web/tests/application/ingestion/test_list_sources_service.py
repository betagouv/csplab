from application.ingestion.services.list_sources import list_sources
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)


def test_lists_all_sources_ordered_by_slug(db):
    second = SourceDjangoFactory(slug="b-source")
    first = SourceDjangoFactory(slug="a-source")

    assert list(list_sources()) == [first, second]
