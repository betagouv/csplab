from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.services.note_query_service_interface import (
    INoteQueryService,
)
from application.recruteur.usecases.lister_notes_candidature import (
    ListerNotesCandidatureQuery,
    ListerNotesCandidatureUsecase,
)
from infrastructure.factories.recruteur.note_factory import NoteFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture(name="service")
def service_fixture() -> INoteQueryService:
    return cast(INoteQueryService, create_interface_aware_mock(INoteQueryService))


class TestListerNotesCandidature:
    def test_lister_note_returns_active_notes_of_the_candidature(self, service):
        candidature_id = uuid4()
        notes = [NoteFactory.create_read_model(candidature_id=candidature_id)]
        service.get_by_candidature = MagicMock(return_value=notes)
        usecase = ListerNotesCandidatureUsecase(note_query_service=service)

        result = usecase.execute(
            ListerNotesCandidatureQuery(candidature_id=candidature_id)
        )

        assert result == notes
        service.get_by_candidature.assert_called_once_with(candidature_id)

    def test_lister_note_receives_error_from_repository(self, service):
        service.get_by_candidature = MagicMock(side_effect=Exception("db error"))
        usecase = ListerNotesCandidatureUsecase(note_query_service=service)

        with pytest.raises(Exception, match="db error"):
            usecase.execute(ListerNotesCandidatureQuery(candidature_id=uuid4()))
