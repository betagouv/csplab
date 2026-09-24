from uuid import uuid4

import factory
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


def _liste_url(organisme_uuid, recrutement_uuid, candidature_uuid):
    return reverse(
        "recruteur:organisme-recrutement-candidature-documents",
        kwargs={
            "organisme_uuid": organisme_uuid,
            "recrutement_uuid": recrutement_uuid,
            "candidature_uuid": candidature_uuid,
        },
    )


def _liste_unknown_organisme(organisme, recrutement, candidature):
    return uuid4(), recrutement.pk, candidature.pk


def _liste_unknown_recrutement(organisme, recrutement, candidature):
    return organisme.id, uuid4(), candidature.pk


def _liste_recrutement_from_another_organisme(organisme, recrutement, candidature):
    autre_recrutement = RecrutementDjangoFactory(organisme=OrganismeDjangoFactory())
    return organisme.id, autre_recrutement.pk, candidature.pk


def _liste_mismatched_candidature(organisme, recrutement, candidature):
    autre_recrutement = RecrutementDjangoFactory(organisme=organisme)
    autre_candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=autre_recrutement)
    )
    return organisme.id, recrutement.pk, autre_candidature.pk


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
        # FileResponse is a StreamingHttpResponse
        assert b"".join(response.streaming_content) == b"%PDF-1.4\n%test"
        assert response["Content-Type"] == "application/pdf"
        assert response["Content-Disposition"] == 'inline; filename="test.pdf"'

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

        assert response.status_code == status.HTTP_404_NOT_FOUND

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

    def test_returns_415_for_disallowed_content_type(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        document = DocumentDjangoFactory(
            candidature=candidature,
            fichier=factory.django.FileField(
                filename="test.html", data=b"<script></script>"
            ),
        )

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk, document.pk)
        )

        assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


NOMBRE_DOCUMENTS_ATTENDU = 3
NOMBRE_REQUETES_ATTENDU = (
    2  # authentification
    + 1  # organisme
    + 1  # agent's role
    + 1  # matching recrutement with organisme
    + 1  # matching candidature with recrutement
    + 2  # pagination : count + page
)


class TestCandidatureDocumentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_liste_url(uuid4(), uuid4(), uuid4()))

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
    def test_authorized_agent_lists_the_documents(
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
            _liste_url(organisme.id, recrutement.pk, candidature.pk)
        )

        assert response.status_code == status.HTTP_200_OK
        results = response.json()["results"]
        assert len(results) == 1
        assert results[0]["uuid"] == str(document.pk)
        assert results[0]["type"] == document.type_document
        assert results[0]["nom_original"] == document.nom_original
        assert results[0]["content_type"] == document.content_type
        assert results[0]["taille"] == document.taille
        assert results[0]["depose_par_uuid"] == str(document.depose_par_id)
        assert results[0]["depose_par"] == document.depose_par.get_full_name()

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

        response = authenticated_client.get(
            _liste_url(organisme.id, recrutement.pk, candidature.pk)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "build_ids",
        [
            _liste_unknown_organisme,
            _liste_unknown_recrutement,
            _liste_recrutement_from_another_organisme,
            _liste_mismatched_candidature,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
            "mismatched_candidature",
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

        organisme_id, recrutement_id, candidature_id = build_ids(
            organisme, recrutement, candidature
        )

        response = authenticated_client.get(
            _liste_url(organisme_id, recrutement_id, candidature_id)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_supports_page_and_limit_query_params(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        DocumentDjangoFactory.create_batch(
            NOMBRE_DOCUMENTS_ATTENDU, candidature=candidature
        )

        response = authenticated_client.get(
            _liste_url(organisme.id, recrutement.pk, candidature.pk),
            {"page": 2, "limit": 2},
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == NOMBRE_DOCUMENTS_ATTENDU
        assert len(body["results"]) == 1

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, test_user, django_assert_num_queries
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        DocumentDjangoFactory.create_batch(5, candidature=candidature)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = authenticated_client.get(
                _liste_url(organisme.id, recrutement.pk, candidature.pk)
            )

        assert response.status_code == status.HTTP_200_OK
