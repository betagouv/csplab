from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.recruteur.entities.note import Note
from infrastructure.django_apps.recruteur.models import NoteModel


class NoteMapper(IFromDomainMapper, IToDomainMapper):
    def to_domain(self, model: NoteModel) -> Note:
        return Note.build(
            entity_id=model.id,
            candidature_id=model.candidature_id,
            message=model.message,
            publie_par_id=UUID(model.publie_par_id),  # type: ignore[arg-type]
            publie_le=model.created_at,
            mis_a_jour_par_id=UUID(model.mis_a_jour_par_id),  # type: ignore[arg-type]
            mis_a_jour_le=model.updated_at,
            supprimee_par_id=(
                UUID(model.supprimee_par_id)  # type: ignore[arg-type]
                if model.supprimee_par_id
                else None
            ),
            supprimee_le=model.supprimee_le,
        )

    def from_domain(self, note: Note) -> NoteModel:
        # publie_le / mis_a_jour_le are persisted via the auto-managed
        # created_at / updated_at columns on BaseDatedModel.
        return NoteModel(
            id=note.entity_id,
            candidature_id=note.candidature_id,
            message=note.message,
            publie_par_id=str(note.publie_par_id),
            mis_a_jour_par_id=str(note.mis_a_jour_par_id),
            supprimee_par_id=(
                str(note.supprimee_par_id) if note.supprimee_par_id else None
            ),
            supprimee_le=note.supprimee_le,
        )
