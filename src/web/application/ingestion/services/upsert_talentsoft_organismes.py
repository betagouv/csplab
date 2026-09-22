from collections import Counter

from django.db import transaction

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel

UPDATE_FIELDS = [
    "organisme_id",
    "parent_code",
    "has_children",
    "name",
    "description",
    "url",
    "phone_number",
    "post_code",
    "latitude",
    "longitude",
    "parent_name",
    "logo_url",
    "max_delay_for_consent",
    "retention_period",
    "general_conditions",
    "personal_data_consent",
]


def _error(item: dict, message: str) -> dict:
    organisme_id = item["organisme_id"]
    return {
        "talentsoft_organisme": {
            "entity_code": item["entity_code"],
            "organisme_id": str(organisme_id) if organisme_id else None,
        },
        "error": message,
    }


def upsert_talentsoft_organismes(items: list[dict]) -> dict:
    errors: list[dict] = []

    organisme_ids = {
        item["organisme_id"] for item in items if item["organisme_id"] is not None
    }
    existing_organisme_ids = set(
        OrganismeModel.objects.by_organisme_ids(organisme_ids).values_list(
            "id", flat=True
        )
    )

    candidates = []
    for item in items:
        organisme_id = item["organisme_id"]
        if organisme_id is not None and organisme_id not in existing_organisme_ids:
            errors.append(_error(item, "Organisme introuvable."))
            continue
        candidates.append(item)

    entity_code_counts = Counter(item["entity_code"] for item in candidates)
    duplicate_entity_codes = {
        entity_code for entity_code, count in entity_code_counts.items() if count > 1
    }

    valid_items = []
    for item in candidates:
        if item["entity_code"] in duplicate_entity_codes:
            errors.append(_error(item, "entity_code en doublon dans le lot."))
            continue
        valid_items.append(item)

    existing_entity_codes = set(
        TalentsoftOrganismeModel.objects.by_entity_codes(
            [item["entity_code"] for item in valid_items]
        ).values_list("entity_code", flat=True)
    )

    with transaction.atomic():
        TalentsoftOrganismeModel.objects.bulk_create(
            [TalentsoftOrganismeModel(**item) for item in valid_items],
            update_conflicts=True,
            update_fields=UPDATE_FIELDS,
            unique_fields=["entity_code"],
        )

    updated = len(existing_entity_codes)
    created = len(valid_items) - updated

    return {"created": created, "updated": updated, "errors": errors}
