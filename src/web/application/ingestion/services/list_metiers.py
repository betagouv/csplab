from django.db.models import QuerySet

from infrastructure.django_apps.referentiel.models.metier import MetierModel


def list_metiers(*, domain: str | None = None) -> QuerySet[MetierModel]:
    return MetierModel.objects.by_functional_area(domain).stable_order()
