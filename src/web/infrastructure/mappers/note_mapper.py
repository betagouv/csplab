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
            supprimee_le=model.supprimee_le,
        )

    def from_domain(self, note: Note) -> NoteModel:
        # created_at / updated_at columns on BaseDatedModel.
        return NoteModel(
            id=note.entity_id,
            candidature_id=note.candidature_id,
            message=note.message,
            publie_par_id=str(note.publie_par_id),
        )
