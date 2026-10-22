from datetime import UTC, datetime
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from referentiel.value_objects.offer_nature import OfferNature
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.test import APIClient

from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementQuerySet
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.commons.pagination import PageNumberLimitPagination

fake = Faker()

ORGANISME_UUID = fake.uuid4()

RECRUTEMENTS_ACTIFS_URL = reverse(
    "recruteur:organisme_recrutements_actifs",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
RECRUTEMENTS_ARCHIVES_URL = reverse(
    "recruteur:organisme_recrutements_archives",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)

NOMBRE_REQUETES_ACTIFS_ATTENDU = (
    2  # authentication (view + RateLimitHeadersMiddleware)
    + 1  # organisme
    + 1  # agent's role
    + 2  # pagination: count + page
    + 1  # prefetch agents_liaisons
)
NOMBRE_REQUETES_ARCHIVES_ATTENDU = (
    NOMBRE_REQUETES_ACTIFS_ATTENDU
    + 2  # prefetch etapes_acceptees + nested candidatures
)
NB_RECRUTEMENTS_REQUETES = 5

TOTAL = 6
PAGE_SIZE = 2

# (url name, archived)
LISTS = [
    pytest.param(
        "recruteur:organisme_recrutements_actifs",
        False,
        id="actifs",
    ),
    pytest.param(
        "recruteur:organisme_recrutements_archives",
        True,
        id="archives",
    ),
]


def _url(name: str, organisme_id) -> str:
    return reverse(name, kwargs={"organisme_uuid": str(organisme_id)})


def _client_for(utilisateur) -> APIClient:
    client = APIClient()
    client.force_login(utilisateur)
    return client


@pytest.fixture(name="organisme")
def organisme_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR,
        utilisateur=test_user,
        id=UUID(ORGANISME_UUID),
    )
    return organisme


@pytest.mark.parametrize(("name", "archived"), LISTS)
class TestRecrutementsListViews:
    def test_anonymous_access_is_unauthorized(self, api_client, name, archived):
        response = api_client.get(_url(name, ORGANISME_UUID))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unknown_organisme_returns_404(self, authenticated_client, name, archived):
        response = authenticated_client.get(_url(name, uuid4()))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_unexpected_error_returns_500(
        self, authenticated_client, organisme, name, archived
    ):
        with patch.object(
            RecrutementQuerySet, "with_responsables", side_effect=Exception("boom")
        ):
            response = authenticated_client.get(_url(name, organisme.id))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @pytest.mark.parametrize(
        ("demandeur", "expected_status"),
        [
            ("actif", status.HTTP_200_OK),
            ("revoque", status.HTTP_403_FORBIDDEN),
            ("jamais_rattache", status.HTTP_403_FORBIDDEN),
        ],
        ids=["actif", "revoque", "jamais_rattache"],
    )
    def test_requires_active_organisme_liaison(
        self, db, name, archived, demandeur, expected_status
    ):
        organisme = OrganismeDjangoFactory()
        agents = {
            "actif": OrganismeAgentDjangoFactory(organisme=organisme).agent,
            "revoque": OrganismeAgentDjangoFactory(
                organisme=organisme, date_revocation=timezone.now()
            ).agent,
            "jamais_rattache": AgentDjangoFactory(),
        }
        # Rôle de recrutement pour tous : sans liaison active, il ne suffit pas.
        RecrutementDjangoFactory(
            organisme=organisme,
            offre_archivee=archived,
            agent_link__agent=agents[demandeur],
        )
        RecrutementDjangoFactory(organisme=organisme, offre_archivee=archived)

        response = _client_for(agents[demandeur].utilisateur).get(
            _url(name, organisme.id)
        )

        assert response.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            assert response.json()["count"] == 1
        else:
            assert response.json() == {"error": "Forbidden."}

    def test_pagination_second_page(
        self, authenticated_client, organisme, name, archived
    ):
        for _ in range(TOTAL):
            RecrutementDjangoFactory(offre_archivee=archived, organisme=organisme)

        with patch.object(PageNumberPagination, "page_size", PAGE_SIZE):
            response = authenticated_client.get(_url(name, organisme.id) + "?page=2")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == TOTAL
        assert len(data["results"]) == PAGE_SIZE
        assert data["next"] is not None
        assert data["previous"] is not None

    def test_limit_query_param_sets_page_size(
        self, authenticated_client, organisme, name, archived
    ):
        RecrutementDjangoFactory.create_batch(
            TOTAL, organisme=organisme, offre_archivee=archived
        )

        response = authenticated_client.get(
            _url(name, organisme.id), {"limit": PAGE_SIZE}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == TOTAL
        assert len(data["results"]) == PAGE_SIZE

    def test_limit_query_param_is_capped(
        self, authenticated_client, organisme, name, archived
    ):
        RecrutementDjangoFactory.create_batch(
            TOTAL, organisme=organisme, offre_archivee=archived
        )

        with patch.object(PageNumberLimitPagination, "max_page_size", PAGE_SIZE):
            response = authenticated_client.get(
                _url(name, organisme.id), {"limit": TOTAL}
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == TOTAL
        assert len(data["results"]) == PAGE_SIZE

    def test_superviseur_gets_every_recrutement_action(
        self, authenticated_client, organisme, name, archived
    ):
        RecrutementDjangoFactory(organisme=organisme, offre_archivee=archived)

        response = authenticated_client.get(_url(name, organisme.id))

        assert response.status_code == status.HTTP_200_OK
        actions = response.json()["results"][0]["authorized_actions"]
        assert OrganismeAction.REVOKE_RECRUTEMENT_AGENT.value in actions
        assert OrganismeAction.REPLY_CONVERSATION.value in actions
        assert OrganismeAction.LIST_RECRUTEMENTS.value not in actions
        assert actions == sorted(
            actions, key=[action.value for action in OrganismeAction].index
        )

    def test_agent_actions_depend_on_the_role_on_each_recrutement(
        self, db, name, archived
    ):
        organisme = OrganismeDjangoFactory()
        agent = OrganismeAgentDjangoFactory(organisme=organisme).agent
        as_responsable = RecrutementDjangoFactory(
            organisme=organisme,
            offre_archivee=archived,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )
        as_contributeur = RecrutementDjangoFactory(
            organisme=organisme,
            offre_archivee=archived,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )

        response = _client_for(agent.utilisateur).get(_url(name, organisme.id))

        assert response.status_code == status.HTTP_200_OK
        actions = {
            result["uuid"]: result["authorized_actions"]
            for result in response.json()["results"]
        }
        responsable_actions = actions[str(as_responsable.offre_id)]
        contributeur_actions = actions[str(as_contributeur.offre_id)]
        assert OrganismeAction.UPDATE_RECRUTEMENT_ETAPES.value in responsable_actions
        assert (
            OrganismeAction.UPDATE_RECRUTEMENT_ETAPES.value not in contributeur_actions
        )
        assert OrganismeAction.GET_RECRUTEMENT.value in contributeur_actions


class TestRecrutementsActifsView:
    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, organisme, django_assert_num_queries
    ):
        RecrutementDjangoFactory.create_batch(
            NB_RECRUTEMENTS_REQUETES, organisme=organisme
        )

        with django_assert_num_queries(NOMBRE_REQUETES_ACTIFS_ATTENDU):
            response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == NB_RECRUTEMENTS_REQUETES

    def test_returns_persisted_actifs(self, authenticated_client, organisme):
        offer = OfferDjangoFactory(
            archived_at=None, offer_nature=OfferNature.TERRITORIAL.value
        )
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            offre=offer,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
            etapes=EtapeRecrutementFactory.create_entity_batch(),
        )
        membre = recrutement.agents_liaisons.get().agent
        RecrutementDjangoFactory(offre_archivee=True, organisme=organisme)
        for categorie in (
            CategorieEtapeRecrutement.ENTREE,
            CategorieEtapeRecrutement.EN_COURS,
        ):
            CandidatureDjangoFactory(
                etape=EtapeModel.objects.filter(
                    recrutement_id=recrutement.offre_id, categorie=categorie.value
                ).first()
            )

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        result = data["results"][0]
        assert result["uuid"] == str(offer.id)
        assert result["intitule"] == offer.title
        assert result["reference_csp"] == (offer.code_emploi_csp or "")
        assert result["nature_offre"] == offer.offer_nature
        assert result["responsables"] == [{"nom": membre.utilisateur.get_full_name()}]
        assert result["candidatures"] == {"total": 2, "a_traiter": 1, "en_cours": 1}
        assert result["unread_conversations"] == 0
        assert "date_publication" in result
        assert "derniere_activite" in result


class TestRecrutementsArchivesView:
    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, organisme, django_assert_num_queries
    ):
        recrutements = RecrutementDjangoFactory.create_batch(
            NB_RECRUTEMENTS_REQUETES, organisme=organisme, offre_archivee=True
        )
        for recrutement in recrutements:
            CandidatureDjangoFactory(
                etape=recrutement.etapes.get(
                    categorie=CategorieEtapeRecrutement.ACCEPTE.value
                )
            )

        with django_assert_num_queries(NOMBRE_REQUETES_ARCHIVES_ATTENDU):
            response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == NB_RECRUTEMENTS_REQUETES
        assert all(result["recrute"] for result in data["results"])

    def test_returns_persisted_archives(self, authenticated_client, organisme):
        offer = OfferDjangoFactory(
            archived_at=datetime(2025, 6, 1, tzinfo=UTC),
            offer_nature=OfferNature.TERRITORIAL.value,
        )
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            offre=offer,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )
        membre = recrutement.agents_liaisons.get().agent
        RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(
            etape=EtapeModel.objects.filter(
                recrutement_id=recrutement.offre_id,
                categorie=CategorieEtapeRecrutement.ACCEPTE.value,
            ).first()
        )

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        result = data["results"][0]
        assert result["uuid"] == str(offer.id)
        assert result["intitule"] == offer.title
        assert result["reference_csp"] == (offer.code_emploi_csp or "")
        assert result["nature_offre"] == offer.offer_nature
        assert result["responsables"] == [{"nom": membre.utilisateur.get_full_name()}]
        assert result["finalise"] is True
        assert result["recrute"] == candidature.candidat.utilisateur.get_full_name()
        assert result["unread_conversations"] == 0
        assert result["date_archivage"].startswith("2025-06-01")

    def test_recrute_is_null_without_accepted_candidature(
        self, authenticated_client, organisme
    ):
        RecrutementDjangoFactory(organisme=organisme, offre_archivee=True)

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["results"][0]
        assert result["finalise"] is False
        assert result["recrute"] is None
