from datetime import datetime
from uuid import UUID

from django.utils import timezone

from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.django_apps.recruteur.models import NoteModel
from infrastructure.mappers.note_mapper import NoteMapper


class PostgresNoteRepository(INoteRepository):
    def __init__(self) -> None:
        self._mapper = NoteMapper()

    def create(self, note: Note) -> Note:
        model = self._mapper.from_domain(note)
        model.save()
        return note

    def get_by_id(self, note_id: UUID) -> Note:
        try:
            model = NoteModel.objects.get(id=note_id, supprimee_le__isnull=True)
        except NoteModel.DoesNotExist as error:
            raise NoteIntrouvable(note_id) from error
        return self._mapper.to_domain(model)

    def save(self, note: Note) -> None:
        NoteModel.objects.filter(id=note.entity_id).update(
            message=note.message,
            updated_at=timezone.make_aware(datetime.now()),
        )

    def delete(self, note_id: UUID) -> None:
        NoteModel.objects.filter(id=note_id).update(
            supprimee_le=timezone.make_aware(datetime.now()),
            updated_at=timezone.make_aware(datetime.now()),
        )
