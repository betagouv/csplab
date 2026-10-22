from datetime import datetime, timezone

from referentiel.value_objects.verse import Verse

from application.ingestion.services.list_public_organismes import (
    list_public_organismes,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)


def _localisation(department: str) -> dict:
    return {"area": "EU", "country": "FRA", "region": "94", "department": department}


def test_excludes_deleted_organismes_and_orders_by_name(db):
    second = OrganismeDjangoFactory(nom="Mairie de Lyon")
    first = OrganismeDjangoFactory(nom="CHU de Bordeaux")
    OrganismeDjangoFactory(
        nom="Préfecture", supprime_le=datetime(2026, 1, 1, tzinfo=timezone.utc)
    )

    assert list(list_public_organismes()) == [first, second]


def test_combines_filters(db):
    expected = OrganismeDjangoFactory(
        nom="Centre hospitalier de Bastia",
        versant=Verse.FPH.value,
        referentiel="FINESS",
        localisation=_localisation("2B"),
    )
    OrganismeDjangoFactory(
        nom="Centre hospitalier d'Ajaccio",
        versant=Verse.FPH.value,
        referentiel="FINESS",
        localisation=_localisation("2A"),
    )
    OrganismeDjangoFactory(nom="Mairie de Bastia", versant=Verse.FPT.value)

    result = list_public_organismes(
        versants=[Verse.FPH],
        name="hospitalier",
        department="2B",
        referentiel="FINESS",
    )

    assert list(result) == [expected]
