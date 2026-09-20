from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from domain.recruteur.entities.note import Note
from domain.recruteur.events.note_events import (
    NoteAjoutee,
    NoteEditee,
    NoteSupprimee,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)






