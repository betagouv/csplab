from uuid import UUID

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


class OfferOrganismes:
    # Shared by the offers of a batch: they often come from the same organisme,
    # which is then looked up once.
    def __init__(self) -> None:
        self._organisme_ids: dict[str, UUID | None] = {}
        self._talentsoft_entity_codes: dict[str, bool] = {}

    def organisme_id(self, siret: str) -> UUID | None:
        if siret not in self._organisme_ids:
            self._organisme_ids[siret] = (
                OrganismeModel.objects.actives()
                .by_siret(siret)
                .values_list("id", flat=True)
                .first()
            )
        return self._organisme_ids[siret]

    def talentsoft_organisme_exists(self, entity_code: str) -> bool:
        if entity_code not in self._talentsoft_entity_codes:
            self._talentsoft_entity_codes[entity_code] = (
                TalentsoftOrganismeModel.objects.by_entity_code(entity_code).exists()
            )
        return self._talentsoft_entity_codes[entity_code]
