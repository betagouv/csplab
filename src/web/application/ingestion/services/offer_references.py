import re
from collections.abc import Iterable
from uuid import UUID

from infrastructure.django_apps.referentiel.models.offer import OfferModel

GENERATED_REFERENCE = re.compile(r"CSP-\d{4}-\d{6,}")


def format_reference(year: int, number: int) -> str:
    return f"CSP-{year}-{number:06d}"


def is_generated_reference(reference: str) -> bool:
    return GENERATED_REFERENCE.fullmatch(reference) is not None


def unknown_generated_references(
    source_id: UUID, references: Iterable[str]
) -> set[str]:
    generated = {
        reference for reference in references if is_generated_reference(reference)
    }
    if not generated:
        return set()
    existing = (
        OfferModel.objects.by_source(source_id)
        .by_references(generated)
        .values_list("reference", flat=True)
    )
    return generated - set(existing)
