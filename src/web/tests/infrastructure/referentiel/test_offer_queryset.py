from datetime import datetime, timezone

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

NOW = datetime.now(timezone.utc)


def test_by_source_includes_archived_offers(db):
    source = SourceDjangoFactory()
    active_offer = OfferDjangoFactory(source=source)
    archived_offer = OfferDjangoFactory(source=source, archived_at=NOW)
    OfferDjangoFactory()  # other source

    offers = OfferModel.objects.by_source(source.source_id)

    assert set(offers) == {active_offer, archived_offer}


def test_actives_excludes_archived_offers(db):
    source = SourceDjangoFactory()
    active_offer = OfferDjangoFactory(source=source)
    OfferDjangoFactory(source=source, archived_at=NOW)
    OfferDjangoFactory()  # other source

    offers = OfferModel.objects.by_source(source.source_id).actives()

    assert list(offers) == [active_offer]


def test_by_references(db):
    offer = OfferDjangoFactory(reference="REF-1")
    OfferDjangoFactory(reference="REF-2")

    offers = OfferModel.objects.by_references(["REF-1", "REF-3"])

    assert list(offers) == [offer]
