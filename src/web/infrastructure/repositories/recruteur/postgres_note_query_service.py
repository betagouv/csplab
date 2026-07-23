from uuid import UUID

from application.recruteur.dtos.note_read_models import NoteReadModel
from application.recruteur.services.note_query_service_interface import (
    INoteQueryService,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel


class PostgresNoteQueryService(INoteQueryService):
    def get_by_candidature(self, candidature_id: UUID) -> list[NoteReadModel]:
        models = (
            NoteModel.objects.filter(
                candidature_id=candidature_id,
                supprimee_le__isnull=True,
            )
            .select_related("publie_par__utilisateur")
            .order_by("-created_at")
        )
        return [
            NoteReadModel(
                entity_id=model.id,
                candidature_id=model.candidature_id,
                message=model.message,
                publie_par_id=UUID(model.publie_par_id),  # type: ignore[arg-type]
                publie_par_prenom=model.publie_par.utilisateur.first_name,
                publie_par_nom=model.publie_par.utilisateur.last_name,
                publie_le=model.created_at,
            )
            for model in models
        ]
