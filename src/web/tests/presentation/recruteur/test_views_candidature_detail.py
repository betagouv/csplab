import logging
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from application.identite.context_services.permission_service import (
    PermissionService,
)
from config.logger_names import LoggerName
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.tag.models import CandidatureTagModel, TagColor
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
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    TagDjangoFactory,
)

NOMBRE_CANDIDATURES_ETAPE = 5
NOMBRE_REQUETES_ATTENDU = (
    2  # authentication (view + RateLimitHeadersMiddleware)
    + 1  # organisme
    + 1  # agent's role
    + 1  # recrutement belongs to organisme (exists check)
    + 1  # agent's role on the recrutement
    + 1  # candidature + candidat, utilisateur, etape, recrutement, offre
    + 1  # prefetch recrutement etapes
    + 1  # prefetch tags_liaisons (tag via select_related)
    + 1  # latest CV
    + 1  # navigation within the etape
)
CANDIDAT_TELEPHONE = "+33 6 98 76 54 32"
CANDIDAT_VILLE = "Saint-Pierre-des-Corps"


def _set_contact(candidature) -> None:
    candidat = candidature.candidat
    candidat.telephone = CANDIDAT_TELEPHONE
    candidat.ville = CANDIDAT_VILLE
    candidat.save(update_fields=["telephone", "ville"])


@pytest.fixture
def emitted_log_records(monkeypatch, caplog):
    for logger_name in (None, *settings.LOGGING["loggers"]):
        caplog.set_level(logging.DEBUG, logger=logger_name)
    records = []
    handle = logging.Logger.handle

    def record_then_handle(logger, record):
        records.append(record)
        handle(logger, record)

    monkeypatch.setattr(logging.Logger, "handle", record_then_handle)
    return records


def _detail_url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:organisme_recrutement_candidature_detail",
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
        assert response.json() == {"error": "Cette candidature n'est pas accessible."}

    def test_returns_candidature_detail(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        cv = DocumentDjangoFactory(candidature=candidature)
        utilisateur = candidature.candidat.utilisateur
        _set_contact(candidature)

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
            "telephone": CANDIDAT_TELEPHONE,
            "ville": CANDIDAT_VILLE,
        }
        assert data["recrutement_intitule"] == recrutement.offre.title
        assert data["etape_actuelle"] == {
            "uuid": str(candidature.etape_id),
            "nom": candidature.etape.nom,
        }
        assert data["motif_refus"] is None
        assert data["date_derniere_maj_candidat"] is None
        assert data["document_uuid"] == str(cv.id)
        assert data["navigation_candidature_uuids"] == [str(candidature.id)]

    def test_returns_null_contact_when_profil_has_none(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        candidat = response.json()["candidat"]
        assert candidat["telephone"] is None
        assert candidat["ville"] is None

    def test_does_not_log_candidat_contact(
        self, authenticated_client, test_user, emitted_log_records
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        _set_contact(candidature)

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )
        logging.getLogger(LoggerName.RECRUTEUR.value).debug("témoin")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["candidat"]["telephone"] == CANDIDAT_TELEPHONE
        logged = [logging.Formatter().format(record) for record in emitted_log_records]
        assert "témoin" in logged
        assert [
            line
            for line in logged
            if CANDIDAT_TELEPHONE in line or CANDIDAT_VILLE in line
        ] == []

    def test_superviseur_gets_authorized_actions_of_the_recrutement(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.json()["authorized_actions"] == [
            action.value
            for action in PermissionService().authorized_actions_recrutement(
                AgentOrganismeRole.SUPERVISEUR, recrutement_role=None
            )
        ]

    @pytest.mark.parametrize("recrutement_role", list(AgentRecrutementRole))
    def test_agent_authorized_actions_derive_from_recrutement_role(
        self, authenticated_client, test_user, recrutement_role
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(
                role=AgentOrganismeRole.AGENT, utilisateur=test_user
            )
        )
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=agent, role=recrutement_role.value
        )

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["authorized_actions"] == [
            action.value
            for action in PermissionService().authorized_actions_recrutement(
                AgentOrganismeRole.AGENT, recrutement_role=recrutement_role
            )
        ]

    def test_returns_motif_refus_of_refused_candidature(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        candidature.etape = EtapeModel.objects.get(
            recrutement=recrutement, categorie=CategorieEtapeRecrutement.REFUS.value
        )
        candidature.motif_refus = MotifRefus.EXPERIENCE_INSUFFISANTE
        candidature.save(update_fields=["etape", "motif_refus"])

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.json()["motif_refus"] == {
            "value": "experience_insuffisante",
            "label": "Expérience insuffisante",
        }

    def test_returns_tags_in_pose_order(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        alpha = TagDjangoFactory(
            organisme=organisme, name="Alpha", color=TagColor.ROUGE
        )
        bravo = TagDjangoFactory(organisme=organisme, name="Bravo", color=TagColor.VERT)
        CandidatureTagDjangoFactory(candidature=candidature, tag=alpha)
        bravo_pose = CandidatureTagDjangoFactory(candidature=candidature, tag=bravo)
        CandidatureTagModel.objects.filter(pk=bravo_pose.pk).update(
            created_at=datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        )

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.json()["tags"] == [
            {"uuid": str(bravo.id), "name": "Bravo", "color": "vert"},
            {"uuid": str(alpha.id), "name": "Alpha", "color": "rouge"},
        ]

    def test_staff_without_organisme_role_gets_candidature_detail(
        self, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save(update_fields=["is_staff"])
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )

        response = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk, candidature.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["uuid"] == str(candidature.id)

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, test_user, django_assert_num_queries
    ):
        _, organisme, recrutement, _candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        etape = recrutement.etapes.get(id=recrutement.ordre_etapes[0])
        candidature, *_ = CandidatureDjangoFactory.create_batch(
            NOMBRE_CANDIDATURES_ETAPE, etape=etape
        )
        DocumentDjangoFactory.create_batch(3, candidature=candidature)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = authenticated_client.get(
                _detail_url(organisme.id, recrutement.pk, candidature.id)
            )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["etapes"]) == len(recrutement.ordre_etapes)
        assert len(response.json()["navigation_candidature_uuids"]) == (
            NOMBRE_CANDIDATURES_ETAPE
        )
