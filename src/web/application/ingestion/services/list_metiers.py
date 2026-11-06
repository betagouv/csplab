from django.db.models import QuerySet

from infrastructure.django_apps.referentiel.models.metier import MetierModel


def list_metiers(
    *,
    domains: list[str] | None = None,
    codes: list[str] | None = None,
    active: bool | None = None,
    versant: str | None = None,
) -> QuerySet[MetierModel]:
    return (
        MetierModel.objects.by_functional_areas(domains)
        .by_offer_family_codes(codes)
        .by_active(active)
        .by_versant(versant)
        .stable_order()
    )
