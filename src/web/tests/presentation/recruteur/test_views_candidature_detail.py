from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)


def _detail_url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:organisme-recrutement-candidature-detail",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
        },
    )


def _caller_without_organisme_role(test_user):
    _, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=None)
    )
    return _detail_url(organisme.id, recrutement.pk, candidature.id)


def _agent_not_member_of_recrutement(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return _detail_url(organisme.id, recrutement.pk, candidature.id)


def _unknown_organisme(test_user):
    return _detail_url(uuid4(), uuid4(), uuid4())


def _recrutement_not_in_organisme(test_user):
    _, organisme, _recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    return _detail_url(organisme.id, RecrutementDjangoFactory().pk, candidature.id)


def _candidature_not_in_recrutement(test_user):
    _, organisme, recrutement, _candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    return _detail_url(organisme.id, recrutement.pk, CandidatureDjangoFactory().id)


class TestCandidatureDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _detail_url(uuid4(), uuid4(), uuid4())

        assert api_client.get(url).status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "build_url",
        [
            pytest.param(
                _caller_without_organisme_role, id="caller_without_organisme_role"
            ),
            pytest.param(
                _agent_not_member_of_recrutement, id="agent_not_member_of_recrutement"
            ),
            pytest.param(_unknown_organisme, id="unknown_organisme"),
            pytest.param(
                _recrutement_not_in_organisme, id="recrutement_not_in_organisme"
            ),
            pytest.param(
                _candidature_not_in_recrutement, id="candidature_not_in_recrutement"
            ),
        ],
    )
    def test_denied_access_is_not_found(
        self, authenticated_client, test_user, build_url
    ):
        response = authenticated_client.get(build_url(test_user))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_candidature_detail(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        cv = DocumentDjangoFactory(candidature=candidature)
        utilisateur = candidature.candidat.utilisateur

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["uuid"] == str(candidature.id)
        assert data["candidat"] == {
            "uuid": str(candidature.candidat_id),
            "prenom": utilisateur.first_name,
            "nom": utilisateur.last_name,
            "email": utilisateur.email,
        }
        assert data["recrutement_intitule"] == recrutement.offre.title
        assert data["etape_actuelle"] == {
            "etape_uuid": str(candidature.etape_id),
            "nom": candidature.etape.nom,
        }
        assert data["date_derniere_maj_candidat"] is None
        assert data["document_uuid"] == str(cv.id)
        assert data["navigation_candidature_uuids"] == [str(candidature.id)]
