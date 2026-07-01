from uuid import UUID

from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import CandidatureIntrouvable, NoteIntrouvable
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models import NoteModel
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.mappers.note_mapper import NoteMapper


class PostgresNoteRepository(INoteRepository):
    def __init__(self) -> None:
        self._mapper = NoteMapper()

    def create(self, note: Note) -> Note:
        if not CandidatureModel.objects.filter(id=note.candidature_id).exists():
            raise CandidatureIntrouvable(note.candidature_id)
        if not ProfilAgentModel.objects.filter(
            utilisateur_id=str(note.publie_par_id)  # type: ignore[misc]  # to_field='username' (VARCHAR)
        ).exists():
            raise ProfilAgentNexistePas(note.publie_par_id)
        model = self._mapper.from_domain(note)
        model.save()
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
        model.save()

    def list_by_candidature(self, candidature_id: UUID) -> list[Note]:
        models = NoteModel.objects.filter(
            candidature_id=candidature_id,
            supprimee_le__isnull=True,
        ).order_by("-created_at")
        return [self._mapper.to_domain(model) for model in models]
