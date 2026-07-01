from uuid import UUID

from ddd.domain_errors import DomainError


class NoteError(DomainError):
    pass


class NoteIntrouvable(NoteError):
    def __init__(self, note_id: UUID):
        super().__init__(f"La note {note_id} est introuvable")


class CandidatureIntrouvable(NoteError):
    def __init__(self, candidature_id: UUID):
        self.candidature_id = candidature_id
        super().__init__(f"La candidature {candidature_id} est introuvable")


class NoteModificationNonAutorisee(NoteError):
    def __init__(self, note_id: UUID):
        super().__init__(f"La note {note_id} ne peut être modifiée que par son auteur")


class NoteSuppressionNonAutorisee(NoteError):
    def __init__(self, note_id: UUID):
        super().__init__(f"La note {note_id} ne peut être supprimée que par son auteur")
