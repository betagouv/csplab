from datetime import timedelta
from uuid import uuid4

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)


def _notes_url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:candidature-notes",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
        },
    )


def _note_detail_url(organisme_id, recrutement_id, candidature_id, note_id) -> str:
    return reverse(
        "recruteur:candidature-note-detail",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
            "note_uuid": str(note_id),
        },
    )


class TestCandidatureNotesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _notes_url(uuid4(), uuid4(), uuid4())

        assert api_client.get(url).status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_recrutement_not_in_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        _, organisme, _recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        other_recrutement = RecrutementDjangoFactory()

        response = authenticated_client.get(
            _notes_url(organisme.id, other_recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_candidature_not_in_recrutement_is_not_found(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, _candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        other_candidature = CandidatureDjangoFactory()

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, other_candidature.id)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_notes_newest_first_without_deleted_ones(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        older = NoteDjangoFactory(candidature=candidature, message="a")
        newer = NoteDjangoFactory(candidature=candidature, message="b")
        NoteDjangoFactory(
            candidature=candidature, message="supprimée", supprimee_le=timezone.now()
        )
        NoteModel.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert [n["entity_id"] for n in response.json()["results"]] == [
            str(newer.id),
            str(older.id),
        ]

    def test_post_requires_message(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.post(
            _notes_url(organisme.id, recrutement.pk, candidature.id),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_persisted_notes(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, message="Bon profil")

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["results"]
        assert len(data) == 1
        assert data[0]["entity_id"] == str(note.id)
        assert data[0]["message"] == "Bon profil"
        assert data[0]["publie_par_id"] == str(note.publie_par_id)
        assert data[0]["publie_par_prenom"] == note.publie_par.utilisateur.first_name
        assert data[0]["publie_par_nom"] == note.publie_par.utilisateur.last_name

    def test_post_creates_and_persists_the_note(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.post(
            _notes_url(organisme.id, recrutement.pk, candidature.id),
            data={"message": "Nouvelle note"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "Nouvelle note"
        assert data["candidature_id"] == str(candidature.id)
        assert data["publie_par_id"] == str(test_user.username)

        note = NoteModel.objects.get(id=data["entity_id"])
        assert note.message == "Nouvelle note"
        assert str(note.publie_par_id) == str(test_user.username)


class TestCandidatureNoteDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _note_detail_url(uuid4(), uuid4(), uuid4(), uuid4())

        assert api_client.delete(url).status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        note = NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "x"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_requires_message(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_unknown_note(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, uuid4()),
            data={"message": "x"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_note_of_another_author(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, message="avant")

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "après"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=note.id).message == "avant"

    def test_patch_note_of_another_candidature(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(publie_par=agent, message="avant")

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "après"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=note.id).message == "avant"

    def test_delete_unknown_note(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.delete(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, uuid4())
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_of_another_author(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.delete(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=note.id).supprimee_le is None

    def test_patch_updates_and_persists_the_note(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "Message modifié"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Message modifié"
        assert NoteModel.objects.get(id=note.id).message == "Message modifié"

    def test_delete_removes_the_note(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.delete(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id)
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert NoteModel.objects.get(id=note.id).supprimee_le is not None
