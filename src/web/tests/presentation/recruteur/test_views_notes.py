from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.usecases.creer_note import CreerNoteCommand
from application.recruteur.usecases.editer_note import EditerNoteCommand
from application.recruteur.usecases.supprimer_note import SupprimerNoteCommand
from domain.candidate.exceptions.candidature_errors import CandidatureIntrouvable
from domain.recruteur.errors.note_errors import NoteIntrouvable
from infrastructure.factories.recruteur.note_factory import NoteFactory

fake = Faker()

CANDIDATURE_UUID = str(fake.uuid4())
NOTE_UUID = str(fake.uuid4())

NOTES_URL = reverse(
    "recruteur:candidature-notes",
    kwargs={"candidature_uuid": CANDIDATURE_UUID},
)
NOTE_DETAIL_URL = reverse(
    "recruteur:candidature-note-detail",
    # TODO supprimer candidature_id
    kwargs={"candidature_uuid": CANDIDATURE_UUID, "note_uuid": NOTE_UUID},
)


@pytest.fixture
def container():
    with patch("presentation.recruteur.views.notes.recruteur_container") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestCandidatureNotesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(NOTES_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_notes(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = [
            NoteFactory.create_read_model(message="a"),
            NoteFactory.create_read_model(message="b"),
        ]
        container.lister_notes_candidature_usecase.return_value = mock_usecase

        response = authenticated_client.get(NOTES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [n["message"] for n in response.json()] == ["a", "b"]

    def test_create_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = NoteFactory.create_entity(
            message="nouvelle note"
        )
        container.creer_note_usecase.return_value = mock_usecase

        response = authenticated_client.post(
            NOTES_URL, data={"message": "nouvelle note"}, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "nouvelle note"
        mock_usecase.execute.assert_called_once_with(
            CreerNoteCommand(
                candidature_id=UUID(CANDIDATURE_UUID),
                publie_par_id=UUID(test_user.username),
                message="nouvelle note",
            )
        )

    def test_create_note_requires_message(self, container, authenticated_client):
        container.creer_note_usecase.return_value = MagicMock()

        response = authenticated_client.post(NOTES_URL, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_note_unknown_candidature(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = CandidatureIntrouvable(uuid4())
        container.creer_note_usecase.return_value = mock_usecase

        response = authenticated_client.post(
            NOTES_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestNoteDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert (
            api_client.delete(NOTE_DETAIL_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    def test_edit_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = NoteFactory.create_entity(
            message="modifiée"
        )
        container.editer_note_usecase.return_value = mock_usecase

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "modifiée"}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        mock_usecase.execute.assert_called_once_with(
            EditerNoteCommand(
                note_id=UUID(NOTE_UUID),
                message="modifiée",
                mis_a_jour_par_id=UUID(test_user.username),
            )
        )

    def test_edit_note_not_found(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = NoteIntrouvable(uuid4())
        container.editer_note_usecase.return_value = mock_usecase

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = None
        container.supprimer_note_usecase.return_value = mock_usecase

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_usecase.execute.assert_called_once_with(
            SupprimerNoteCommand(
                note_id=UUID(NOTE_UUID),
                supprime_par_id=UUID(test_user.username),
            )
        )

    def test_delete_note_not_found(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = NoteIntrouvable(uuid4())
        container.supprimer_note_usecase.return_value = mock_usecase

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
