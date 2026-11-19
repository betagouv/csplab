from datetime import UTC, datetime

from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)

NOW = datetime.now(UTC)


def test_filters_combine(db):
    expected = MetierDjangoFactory(
        domaine_fonctionnel_code="JUS", offer_family_code="ERJUS008", versants=["FPE"]
    )
    MetierDjangoFactory(
        domaine_fonctionnel_code="CTL",
        offer_family_code="ERJUS008",
        versants=["FPE"],
        archived_at=NOW,
    )
    MetierDjangoFactory(
        domaine_fonctionnel_code="JUS", offer_family_code="ERJUS008", versants=["FPT"]
    )
    MetierDjangoFactory(
        domaine_fonctionnel_code="JUS", offer_family_code="ERJUS001", versants=["FPE"]
    )
    MetierDjangoFactory(
        domaine_fonctionnel_code="NUM", offer_family_code="ERJUS008", versants=["FPE"]
    )

    metiers = (
        MetierModel.objects.by_functional_areas(["JUS", "CTL"])
        .by_offer_family_codes(["ERJUS008"])
        .by_active(True)
        .by_versant("FPE")
    )

    assert list(metiers) == [expected]


def test_filters_without_value_keep_everything(db):
    metiers = {MetierDjangoFactory(), MetierDjangoFactory(archived_at=NOW)}

    assert (
        set(
            MetierModel.objects.by_functional_areas(None)
            .by_offer_family_codes(None)
            .by_active(None)
            .by_versant(None)
        )
        == metiers
    )
