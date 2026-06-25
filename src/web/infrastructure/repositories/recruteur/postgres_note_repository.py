from uuid import UUID

from django.db import IntegrityError

from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import CandidatureIntrouvable, NoteIntrouvable
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.django_apps.recruteur.models import NoteModel
from infrastructure.mappers.note_mapper import NoteMapper


class PostgresNoteRepository(INoteRepository):
    def __init__(self) -> None:
        self._mapper = NoteMapper()

    def create(self, note: Note) -> Note:
        model = self._mapper.from_domain(note)
        try:
            model.save()
        except IntegrityError as e:
            # SQLSTATE 23503: foreign key violation; the PostgreSQL message
            # carries the offending column name.
            error_detail = str(e)
            if "candidature_id" in error_detail:
                raise CandidatureIntrouvable(note.candidature_id) from e
            if "publie_par_id" in error_detail or "mis_a_jour_par_id" in error_detail:
                raise ProfilAgentNexistePas(note.publie_par_id) from e
            raise
        return note

    def get_by_id(self, note_id: UUID) -> Note:
        try:
            model = NoteModel.objects.get(id=note_id)
        except NoteModel.DoesNotExist as e:
            raise NoteIntrouvable(note_id) from e
        return self._mapper.to_domain(model)

    def save(self, note: Note) -> None:
        try:
            model = NoteModel.objects.get(id=note.entity_id)
        except NoteModel.DoesNotExist as e:
            raise NoteIntrouvable(note.entity_id) from e
        model.message = note.message
        model.mis_a_jour_par_id = str(note.mis_a_jour_par_id)
        model.supprimee_le = note.supprimee_le
        model.supprimee_par_id = (
            str(note.supprimee_par_id) if note.supprimee_par_id else None
        )
        # `updated_at` (mapped to mis_a_jour_le) refreshes via auto_now on save().
        model.save()

    def list_by_candidature(self, candidature_id: UUID) -> list[Note]:
        models = NoteModel.objects.filter(
            candidature_id=candidature_id,
            supprimee_le__isnull=True,
        ).order_by("created_at")
        return [self._mapper.to_domain(model) for model in models]
