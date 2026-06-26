from unittest.mock import MagicMock, patch
from uuid import uuid4

from django.urls import reverse
from rest_framework import status

from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import (
    CandidatureIntrouvable,
    NoteDejaSupprimee,
    NoteIntrouvable,
    NoteModificationNonAutorisee,
    NoteSuppressionNonAutorisee,
)

CANDIDATURE_UUID = str(uuid4())
NOTE_UUID = str(uuid4())

NOTES_URL = reverse(
    "recruteur:candidature-notes",
    kwargs={"candidature_uuid": CANDIDATURE_UUID},
)
NOTE_DETAIL_URL = reverse(
    "recruteur:candidature-note-detail",
    kwargs={"candidature_uuid": CANDIDATURE_UUID, "note_uuid": NOTE_UUID},
)


def _patched_container(**usecases):
    mock_container = MagicMock()
    for name, usecase in usecases.items():
        getattr(mock_container, name).return_value = usecase
    return patch(
        "presentation.recruteur.views.recruteur_container",
        return_value=mock_container,
    )


def _note(message: str = "ma note") -> Note:
    return Note.create(candidature_id=uuid4(), publie_par_id=uuid4(), message=message)


class TestCandidatureNotesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(NOTES_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_notes(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.return_value = [_note("a"), _note("b")]

        with _patched_container(lister_notes_candidature_usecase=usecase):
            response = authenticated_client.get(NOTES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [n["message"] for n in response.json()] == ["a", "b"]

    def test_create_note(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.return_value = _note("nouvelle note")

        with _patched_container(creer_note_usecase=usecase):
            response = authenticated_client.post(
                NOTES_URL, data={"message": "nouvelle note"}, format="json"
            )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "nouvelle note"

    def test_create_note_requires_message(self, authenticated_client):
        with _patched_container(creer_note_usecase=MagicMock()):
            response = authenticated_client.post(NOTES_URL, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_note_unknown_candidature(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = CandidatureIntrouvable(uuid4())

        with _patched_container(creer_note_usecase=usecase):
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

    def test_edit_note(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.return_value = _note("modifiée")

        with _patched_container(editer_note_usecase=usecase):
            response = authenticated_client.patch(
                NOTE_DETAIL_URL, data={"message": "modifiée"}, format="json"
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "modifiée"

    def test_edit_note_not_found(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = NoteIntrouvable(uuid4())

        with _patched_container(editer_note_usecase=usecase):
            response = authenticated_client.patch(
                NOTE_DETAIL_URL, data={"message": "x"}, format="json"
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_note_forbidden_when_not_publisher(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = NoteModificationNonAutorisee(uuid4())

        with _patched_container(editer_note_usecase=usecase):
            response = authenticated_client.patch(
                NOTE_DETAIL_URL, data={"message": "x"}, format="json"
            )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_note(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.return_value = None

        with _patched_container(supprimer_note_usecase=usecase):
            response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_note_not_found(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = NoteIntrouvable(uuid4())

        with _patched_container(supprimer_note_usecase=usecase):
            response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_forbidden_when_not_publisher(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = NoteSuppressionNonAutorisee(uuid4())

        with _patched_container(supprimer_note_usecase=usecase):
            response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_already_deleted(self, authenticated_client):
        usecase = MagicMock()
        usecase.execute.side_effect = NoteDejaSupprimee(uuid4())

        with _patched_container(supprimer_note_usecase=usecase):
            response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_409_CONFLICT
