from datetime import datetime, timezone
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)

INITIAL_MOTIF = MotifRefus.EXPERIENCE_INSUFFISANTE.value


def _url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:organisme_recrutement_candidature_motif_refus",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
        },
    )


def _set_categorie(candidature, categorie, motif_refus=None) -> None:
    etape = EtapeModel.objects.filter(
        recrutement_id=candidature.etape.recrutement_id, categorie=categorie.value
    ).first()
    CandidatureModel.objects.filter(pk=candidature.pk).update(
        etape=etape, motif_refus=motif_refus
    )


def _refuse(candidature) -> None:
    _set_categorie(
        candidature, CategorieEtapeRecrutement.REFUS, motif_refus=INITIAL_MOTIF
    )


def _refused_candidature(role, recrutement_role, utilisateur):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(role=role, utilisateur=utilisateur)
    )
    if recrutement_role is not None:
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=agent, role=recrutement_role.value
        )
    _refuse(candidature)
    return organisme, recrutement, candidature


def _patch(client, organisme, recrutement, candidature, data=None):
    return client.patch(
        _url(organisme.id, recrutement.pk, candidature.id),
        data={"motif_refus": MotifRefus.AUTRE.value} if data is None else data,
        format="json",
    )


def _assert_untouched(candidature, motif=INITIAL_MOTIF) -> None:
    stored = CandidatureModel.objects.get(pk=candidature.pk)
    assert stored.motif_refus == motif
    assert not AuditLogModel.objects.filter(ressource_id=candidature.id).exists()


AUTHORIZED_ROLES = [
    (AgentOrganismeRole.SUPERVISEUR, None),
    (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
    (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
]


class TestCandidatureMotifRefusView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.patch(
            _url(uuid4(), uuid4(), uuid4()),
            data={"motif_refus": MotifRefus.AUTRE.value},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        ("role", "recrutement_role"),
        AUTHORIZED_ROLES,
        ids=["superviseur", "agent_responsable", "agent_recruteur"],
    )
    def test_updates_motif_refus(
        self, authenticated_client, test_user, role, recrutement_role
    ):
        organisme, recrutement, candidature = _refused_candidature(
            role, recrutement_role, test_user
        )
        etape_id = CandidatureModel.objects.get(pk=candidature.pk).etape_id

        response = _patch(authenticated_client, organisme, recrutement, candidature)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"value": "autre", "label": "Autre"}
        candidature.refresh_from_db()
        assert candidature.motif_refus == MotifRefus.AUTRE.value
        assert candidature.etape_id == etape_id
        assert candidature.updated_by_recruteur is not None
        assert AuditLogModel.objects.filter(ressource_id=candidature.id).count() == 1

    def test_same_motif_is_a_no_op(self, authenticated_client, test_user):
        organisme, recrutement, candidature = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )

        response = _patch(
            authenticated_client,
            organisme,
            recrutement,
            candidature,
            data={"motif_refus": INITIAL_MOTIF},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["value"] == INITIAL_MOTIF
        _assert_untouched(candidature)
        candidature.refresh_from_db()
        assert candidature.updated_by_recruteur is None

    def test_contributeur_is_forbidden(self, authenticated_client, test_user):
        organisme, recrutement, candidature = _refused_candidature(
            AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR, test_user
        )

        response = _patch(authenticated_client, organisme, recrutement, candidature)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        _assert_untouched(candidature)

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        _refuse(candidature)

        response = _patch(authenticated_client, organisme, recrutement, candidature)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        _assert_untouched(candidature)

    def test_candidature_of_another_recrutement_is_not_found(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, _ = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )
        _, other = create_recrutement_with_candidature(organisme)
        _refuse(other)

        response = _patch(authenticated_client, organisme, recrutement, other)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        _assert_untouched(other)

    def test_candidature_of_another_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        organisme, _, _ = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )
        other_recrutement, other = create_recrutement_with_candidature()
        _refuse(other)

        response = _patch(authenticated_client, organisme, other_recrutement, other)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        _assert_untouched(other)

    def test_deleted_organisme_is_not_found(self, authenticated_client, test_user):
        organisme, recrutement, candidature = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )
        OrganismeModel.objects.filter(pk=organisme.pk).update(
            supprime_le=datetime.now(tz=timezone.utc)
        )

        response = _patch(authenticated_client, organisme, recrutement, candidature)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        _assert_untouched(candidature)

    def test_candidature_not_refused_is_a_conflict(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, candidature = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )
        _set_categorie(candidature, CategorieEtapeRecrutement.EN_COURS)

        response = _patch(authenticated_client, organisme, recrutement, candidature)

        assert response.status_code == status.HTTP_409_CONFLICT
        _assert_untouched(candidature, motif=None)

    @pytest.mark.parametrize(
        "data", [{}, {"motif_refus": "not_a_real_motif"}], ids=["missing", "unknown"]
    )
    def test_rejects_invalid_motif(self, authenticated_client, test_user, data):
        organisme, recrutement, candidature = _refused_candidature(
            AgentOrganismeRole.SUPERVISEUR, None, test_user
        )

        response = _patch(
            authenticated_client, organisme, recrutement, candidature, data=data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        _assert_untouched(candidature)


class TestUpdateMotifRefusAuthorizedActions:
    @pytest.mark.parametrize(
        ("role", "recrutement_role", "expected"),
        [
            (AgentOrganismeRole.SUPERVISEUR, None, True),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE, True),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR, True),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR, False),
        ],
        ids=["superviseur", "responsable", "recruteur", "contributeur"],
    )
    def test_candidature_detail_exposes_update_motif_refus(
        self, authenticated_client, test_user, role, recrutement_role, expected
    ):
        organisme, recrutement, candidature = _refused_candidature(
            role, recrutement_role, test_user
        )

        response = authenticated_client.get(
            reverse(
                "recruteur:organisme_recrutement_candidature_detail",
                kwargs={
                    "organisme_uuid": str(organisme.id),
                    "recrutement_uuid": str(recrutement.pk),
                    "candidature_uuid": str(candidature.id),
                },
            )
        )

        assert response.status_code == status.HTTP_200_OK
        assert (
            "update_motif_refus" in response.json()["authorized_actions"]
        ) is expected
