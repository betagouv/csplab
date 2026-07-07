from uuid import UUID

from ddd.domain_errors import DomainError


class NoteError(DomainError):
    pass


class NoteIntrouvable(NoteError):
    def __init__(self, note_id: UUID):
        super().__init__(f"La note {note_id} est introuvable")
