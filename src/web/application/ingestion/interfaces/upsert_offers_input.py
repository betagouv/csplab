from dataclasses import dataclass

from referentiel.entities.offer import Offer

from infrastructure.django_apps.users.models import UserModel


@dataclass
class UpsertOffersInput:
    offers: list[Offer]
    user: UserModel | None = None
