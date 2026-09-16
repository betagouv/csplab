from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)


def _url(organisme_uuid, recrutement_uuid, candidature_uuid, document_uuid):
    return reverse(
        "recruteur:organisme-recrutement-candidature-document",
        kwargs={
            "organisme_uuid": organisme_uuid,
            "recrutement_uuid": recrutement_uuid,
            "candidature_uuid": candidature_uuid,
            "document_uuid": document_uuid,
        },
    )


def _unknown_organisme(organisme, recrutement, candidature, document):
    return uuid4(), recrutement.pk, candidature.pk, document.pk


def _unknown_recrutement(organisme, recrutement, candidature, document):
    return organisme.id, uuid4(), candidature.pk, document.pk


def _recrutement_from_another_organisme(organisme, recrutement, candidature, document):
    autre_recrutement = RecrutementDjangoFactory(organisme=OrganismeDjangoFactory())
    return organisme.id, autre_recrutement.pk, candidature.pk, document.pk


def _mismatched_candidature(organisme, recrutement, candidature, document):
    autre_candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return organisme.id, recrutement.pk, autre_candidature.pk, document.pk


def _unknown_document(organisme, recrutement, candidature, document):
    return organisme.id, recrutement.pk, candidature.pk, uuid4()


class TestDocumentView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_url(uuid4(), uuid4(), uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "organisme_role,recrutement_role",
        [
            (AgentOrganismeRole.SUPERVISEUR, None),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR),
        ],
        ids=[
            "superviseur",
            "agent_responsable",
            "agent_recruteur",
            "agent_contributeur",
        ],
    )
    def test_authorized_agent_downloads_the_document(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        _, organisme = create_organisme_with_agent(
            role=organisme_role, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        if recrutement_role is not None:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement,
                agent=test_user.profil_agent,
                role=recrutement_role.value,
            )
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        document = DocumentDjangoFactory(candidature=candidature)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk, document.pk)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content == b"%PDF-1.4\n%test"
        assert response["Content-Type"] == "application/pdf"
        assert "test.pdf" in response["Content-Disposition"]

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.AGENT, None], ids=["no_recrutement_role", "no_role"]
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        document = DocumentDjangoFactory(candidature=candidature)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk, document.pk)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "build_ids",
        [
            _unknown_organisme,
            _unknown_recrutement,
            _recrutement_from_another_organisme,
            _mismatched_candidature,
            _unknown_document,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
            "mismatched_candidature",
            "unknown_document",
        ],
    )
    def test_returns_404_for(self, authenticated_client, test_user, build_ids):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        document = DocumentDjangoFactory(candidature=candidature)

        organisme_id, recrutement_id, candidature_id, document_id = build_ids(
            organisme, recrutement, candidature, document
        )

        response = authenticated_client.get(
            _url(organisme_id, recrutement_id, candidature_id, document_id)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
