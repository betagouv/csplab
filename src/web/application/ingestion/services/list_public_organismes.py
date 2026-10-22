from django.db.models import QuerySet
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


def list_public_organismes(
    *,
    versants: list[Verse] | None = None,
    siret: str | None = None,
    name: str | None = None,
    department: str | None = None,
    referentiel: str | None = None,
) -> QuerySet[OrganismeModel]:
    return (
        OrganismeModel.objects.not_supprimes()
        .by_versants(versants)
        .by_siret(siret)
        .search_name(name)
        .by_department(department)
        .by_referentiel(referentiel)
        .stable_order()
    )
