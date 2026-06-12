from uuid import UUID

from infrastructure.django_apps.users.models import UserModel


class PostgresUserSourceRepository:
    def get_allowed_source_ids(
        self, user: UserModel, source_ids: set[UUID]
    ) -> set[UUID]:
        return set(
            user.sources.filter(source_id__in=source_ids).values_list(
                "source_id", flat=True
            )
        )
