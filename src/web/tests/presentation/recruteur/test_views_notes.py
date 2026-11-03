from datetime import timedelta
from uuid import uuid4

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from presentation.commons.pagination import TaillePageNumberPagination


def _notes_url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:candidature_notes",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
        },
    )


def _note_events(note_id) -> list[str]:
    return list(
        AuditLogModel.objects.filter(
            ressource_kind="Note", ressource_id=note_id
        ).values_list("event_name", flat=True)
    )


def _note_detail_url(organisme_id, recrutement_id, candidature_id, note_id) -> str:
    return reverse(
        "recruteur:candidature_note_detail",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
            "note_uuid": str(note_id),
        },
    )


def _note_visibilite_url(organisme_id, recrutement_id, candidature_id, note_id) -> str:
    return reverse(
        "recruteur:candidature_note_visibilite",
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
        assert [n["uuid"] for n in response.json()["results"]] == [
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
        assert data[0]["uuid"] == str(note.id)
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
        assert data["est_privee"] is False

        note = NoteModel.objects.get(id=data["uuid"])
        assert note.message == "Nouvelle note"
        assert str(note.publie_par_id) == str(test_user.username)

    def test_lists_team_notes_and_my_private_notes_only(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        my_private_note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )
        team_note = NoteDjangoFactory(candidature=candidature)
        NoteDjangoFactory(candidature=candidature, est_privee=True)

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == len(data["results"])
        assert {n["uuid"]: n["est_privee"] for n in data["results"]} == {
            str(my_private_note.id): True,
            str(team_note.id): False,
        }

    @pytest.mark.parametrize(
        ("organisme_role", "recrutement_role"),
        [
            (AgentOrganismeRole.SUPERVISEUR, None),
            *(
                (AgentOrganismeRole.AGENT, recrutement_role)
                for recrutement_role in AgentRecrutementRole
            ),
        ],
    )
    def test_author_gets_update_and_delete_on_own_notes_only(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(
                role=organisme_role, utilisateur=test_user
            )
        )
        if recrutement_role:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement, agent=agent, role=recrutement_role.value
            )
        own_note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        own_private_note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )
        team_note = NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert {
            n["uuid"]: n["authorized_actions"] for n in response.json()["results"]
        } == {
            str(own_note.id): ["update_note", "delete_note"],
            str(own_private_note.id): ["update_note", "delete_note"],
            str(team_note.id): [],
        }

    def test_candidature_without_note_returns_an_empty_page(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"] == []

    def test_taille_paginates_and_computes_actions_page_by_page(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        newest = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        middle = NoteDjangoFactory(candidature=candidature)
        oldest = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        now = timezone.now()
        for note, days in ((newest, 0), (middle, 1), (oldest, 2)):
            NoteModel.objects.filter(pk=note.pk).update(
                created_at=now - timedelta(days=days)
            )
        url = _notes_url(organisme.id, recrutement.pk, candidature.id)

        pages = [
            authenticated_client.get(url, {"taille": 1, "page": page}).json()
            for page in (1, 2, 3)
        ]

        assert [p["count"] for p in pages] == [3, 3, 3]
        assert [
            [(n["uuid"], n["authorized_actions"]) for n in p["results"]] for p in pages
        ] == [
            [(str(newest.id), ["update_note", "delete_note"])],
            [(str(middle.id), [])],
            [(str(oldest.id), ["update_note", "delete_note"])],
        ]
        assert pages[0]["previous"] is None
        assert pages[0]["next"] is not None
        assert pages[2]["next"] is None

    def test_default_page_size_returns_all_notes_of_a_small_list(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        NoteDjangoFactory.create_batch(2, candidature=candidature, publie_par=agent)

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        data = response.json()
        assert data["next"] is None
        assert [n["authorized_actions"] for n in data["results"]] == [
            ["update_note", "delete_note"],
            ["update_note", "delete_note"],
        ]

    def test_taille_is_capped_by_max_page_size(
        self, authenticated_client, test_user, monkeypatch
    ):
        monkeypatch.setattr(TaillePageNumberPagination, "max_page_size", 1)
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        notes_count = 2
        NoteDjangoFactory.create_batch(
            notes_count, candidature=candidature, publie_par=agent
        )

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id), {"taille": 5}
        )

        data = response.json()
        assert data["count"] == notes_count
        assert len(data["results"]) == 1

    def test_page_out_of_range_is_not_found(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id), {"page": 2}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_staff_gets_no_action_on_notes(self, authenticated_client, test_user):
        test_user.is_staff = True
        test_user.save(update_fields=["is_staff"])
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.get(
            _notes_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert [n["authorized_actions"] for n in response.json()["results"]] == [[]]

    def test_post_creates_and_logs_a_private_note(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.post(
            _notes_url(organisme.id, recrutement.pk, candidature.id),
            data={"message": "Pour moi", "est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["est_privee"] is True
        note_id = response.json()["uuid"]
        assert NoteModel.objects.get(id=note_id).est_privee is True
        assert _note_events(note_id) == ["NoteAjoutee"]


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

    def test_delete_logs_a_private_note(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )

        response = authenticated_client.delete(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id)
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert NoteModel.objects.get(id=note.id).supprimee_le is not None
        assert _note_events(note.id) == ["NoteSupprimee"]

    def test_patch_without_est_privee_keeps_note_private(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "Message modifié"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is True
        assert NoteModel.objects.get(id=note.id).est_privee is True
        assert _note_events(note.id) == ["NoteEditee"]

    def test_patch_shares_a_private_note(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "Pour l'équipe", "est_privee": False},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is False
        assert NoteModel.objects.get(id=note.id).est_privee is False
        assert _note_events(note.id) == ["NotePartagee"]

    def test_patch_keeps_a_team_note_for_me_and_logs_an_edit(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "Pour moi", "est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is True
        assert NoteModel.objects.get(id=note.id).est_privee is True
        assert _note_events(note.id) == ["NoteEditee"]

    def test_patch_team_note_staying_shared_logs_an_edit(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.patch(
            _note_detail_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"message": "Message modifié", "est_privee": False},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is False
        assert _note_events(note.id) == ["NoteEditee"]


class TestCandidatureNoteVisibiliteView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _note_visibilite_url(uuid4(), uuid4(), uuid4(), uuid4())

        response = api_client.put(url, data={"est_privee": True}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        note = NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_requires_est_privee(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "est_privee" in response.json()

    def test_note_of_another_author_is_not_found(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature)

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=note.id).est_privee is False

    def test_deleted_note_is_not_found(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, supprimee_le=timezone.now()
        )

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_keeps_a_team_note_for_me_and_logs_an_edit(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": True},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is True
        assert NoteModel.objects.get(id=note.id).est_privee is True
        assert _note_events(note.id) == ["NoteEditee"]

    def test_shares_a_private_note(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=True
        )

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": False},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is False
        assert NoteModel.objects.get(id=note.id).est_privee is False
        assert _note_events(note.id) == ["NotePartagee"]

    @pytest.mark.parametrize("est_privee", [True, False])
    def test_same_visibility_changes_nothing(
        self, authenticated_client, test_user, est_privee
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=est_privee
        )
        updated_at = NoteModel.objects.get(id=note.id).updated_at

        response = authenticated_client.put(
            _note_visibilite_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"est_privee": est_privee},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["est_privee"] is est_privee
        assert NoteModel.objects.get(id=note.id).updated_at == updated_at
        assert _note_events(note.id) == []
