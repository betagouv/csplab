from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from infrastructure.django_apps.users.models import UserModel


class PostgresUserSourceRepository:
    def get_allowed_source_ids(
        self, utilisateur: Utilisateur, source_ids: set[UUID]
    ) -> set[UUID]:
        return set(
            UserModel.objects.get(username=str(utilisateur.entity_id))
            .sources.filter(source_id__in=source_ids)
            .values_list("source_id", flat=True)
        )
