from dataclasses import dataclass
from uuid import UUID

from infrastructure.django_apps.users.models import UserModel


@dataclass
class ArchiveOfferByReferenceInput:
    reference: str
    source_id: UUID
    user: UserModel | None = None
