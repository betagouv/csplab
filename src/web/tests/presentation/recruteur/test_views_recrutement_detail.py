from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from faker import Faker
from rest_framework import serializers, status

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.read_conversation import mark_as_read
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.recrutement_errors import (
    CandidatureInexistante,
    MotifRefusRequis,
    RecrutementEtapeInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    ConversationLectureDjangoFactory,
    MessageDjangoFactory,
)
from infrastructure.factories.recruteur.candidature_recruteur_factory import (
    CandidatureRecruteurFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.commons.pagination import TaillePageNumberPagination

fake = Faker()

TAILLE_PAGE = 2
NOMBRE_CANDIDATURES = 5


ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"
UNKNOWN_RECRUTEMENT_UUID = fake.uuid4()

CANDIDATURE_UUID = "aaaaaaaa-0002-0002-0002-000000000002"

RECRUTEMENT_CANDIDATURES_ETAPE_URL = reverse(
    "recruteur:organisme_recrutement_candidatures_etape",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_LISTE_URL = reverse(
    "recruteur:organisme_recrutement_liste",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_DETAIL_URL = reverse(
    "recruteur:organisme_recrutement",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)

NOMBRE_REQUETES_LISTE_ATTENDU = (
    2  # authentication (view + RateLimitHeadersMiddleware)
    + 1  # organisme
    + 1  # agent's role
    + 1  # recrutement with list version
    + 2  # pagination: count + page
    + 1  # etapes
)


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_detail.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


def _detail_url(organisme_id, recrutement_id) -> str:
    return reverse(
        "recruteur:organisme_recrutement",
        kwargs={"organisme_uuid": organisme_id, "recrutement_uuid": recrutement_id},
    )


def _authorized_actions(organisme_role, recrutement_role) -> list[str]:
    permissions = OrganismePermissionService()
    return [
        action.value
        for action in permissions.authorized_actions_recrutement(
            organisme_role, recrutement_role=recrutement_role
        )
    ]


class TestRecrutementDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_detail_payload(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        offre = OfferDjangoFactory(
            title="Chargé de mission numérique", categories=["B", "A"]
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        payload = response.json()
        assert set(payload) == {
            "uuid",
            "intitule",
            "archive",
            "date_publication",
            "localisations",
            "organisme_recruteur",
            "categorie_offre",
            "etapes",
            "recrutement_role",
            "authorized_actions",
        }
        assert payload["recrutement_role"] is None
        assert payload["uuid"] == str(recrutement.pk)
        assert payload["intitule"] == "Chargé de mission numérique"
        assert payload["archive"] is False
        assert payload["categorie_offre"] == "B"
        assert payload["organisme_recruteur"] == {
            "nom": organisme.nom,
            "siret": organisme.siret,
        }
        [localisation] = payload["localisations"]
        assert set(localisation) == {
            "zone_geographique",
            "pays",
            "region",
            "departement",
            "localisation_label",
            "latitude",
            "longitude",
        }

    def test_lists_every_localisation_in_order(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        offre = OfferDjangoFactory(
            localisations=[
                {"area": "EU", "country": "FRA", "region": "28", "department": "14"},
                {"area": "EU", "country": "DEU", "label": "Berlin"},
            ]
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["localisations"] == [
            {
                "zone_geographique": "EU",
                "pays": "FRA",
                "region": "28",
                "departement": "14",
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            },
            {
                "zone_geographique": "EU",
                "pays": "DEU",
                "region": None,
                "departement": None,
                "localisation_label": "Berlin",
                "latitude": None,
                "longitude": None,
            },
        ]

    def test_offre_without_localisation(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        offre = OfferDjangoFactory(localisations=[])
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["localisations"] == []

    def test_etapes_follow_ordre_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        etapes = list(recrutement.etapes.all())
        recrutement.ordre_etapes = [str(etape.id) for etape in reversed(etapes)]
        recrutement.save(update_fields=["ordre_etapes"])

        payload = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk)
        ).json()

        assert [etape["uuid"] for etape in payload["etapes"]] == (
            recrutement.ordre_etapes
        )
        assert set(payload["etapes"][0]) == {"uuid", "nom", "categorie"}
        assert {etape["uuid"]: etape["categorie"] for etape in payload["etapes"]} == {
            str(etape.id): CategorieEtapeRecrutement(etape.categorie).name
            for etape in etapes
        }

    @pytest.mark.parametrize("archivee", [True, False], ids=["archivee", "active"])
    def test_archive_flag_reflects_offre(
        self, authenticated_client, test_user, archivee
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(
            organisme=organisme, offre_archivee=archivee
        )

        payload = authenticated_client.get(
            _detail_url(organisme.id, recrutement.pk)
        ).json()

        assert payload["archive"] is archivee

    @pytest.mark.parametrize(
        ("organisme_role", "recrutement_role", "expected_status"),
        [
            pytest.param(
                AgentOrganismeRole.SUPERVISEUR,
                None,
                status.HTTP_200_OK,
                id="superviseur",
            ),
            *[
                pytest.param(
                    AgentOrganismeRole.AGENT,
                    role,
                    status.HTTP_200_OK,
                    id=f"agent_{role.value}",
                )
                for role in AgentRecrutementRole
            ],
            pytest.param(
                AgentOrganismeRole.AGENT,
                None,
                status.HTTP_403_FORBIDDEN,
                id="agent_sans_role_recrutement",
            ),
        ],
    )
    def test_access_depends_on_roles(
        self,
        authenticated_client,
        test_user,
        organisme_role,
        recrutement_role,
        expected_status,
    ):
        agent, organisme = create_organisme_with_agent(
            role=organisme_role, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        if recrutement_role is not None:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement, agent=agent, role=recrutement_role.value
            )

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == expected_status
        if expected_status == status.HTTP_403_FORBIDDEN:
            assert response.json() == {"error": "Forbidden."}
        else:
            expected_role = recrutement_role.value if recrutement_role else None
            assert response.json()["recrutement_role"] == expected_role
            assert response.json()["authorized_actions"] == _authorized_actions(
                organisme_role, recrutement_role
            )

    def test_staff_gets_detail_without_organisme_role(self, api_client):
        api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
        recrutement = RecrutementDjangoFactory()

        response = api_client.get(_detail_url(recrutement.organisme_id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["authorized_actions"] == _authorized_actions(
            AgentOrganismeRole.SUPERVISEUR, None
        )

    def test_returns_404_for_unknown_recrutement(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )

        response = authenticated_client.get(_detail_url(organisme.id, uuid4()))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_returns_404_for_recrutement_of_another_organisme(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        autre_recrutement = RecrutementDjangoFactory()

        response = authenticated_client.get(
            _detail_url(organisme.id, autre_recrutement.pk)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_number_of_queries_does_not_depend_on_etapes_count(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        petit = RecrutementDjangoFactory(
            organisme=organisme,
            etapes=EtapeRecrutementFactory.create_entity_batch()[:1],
        )
        grand = RecrutementDjangoFactory(organisme=organisme)
        EtapeDjangoFactory.create_batch(5, recrutement=grand)

        with CaptureQueriesContext(connection) as petit_queries:
            authenticated_client.get(_detail_url(organisme.id, petit.pk))
        with CaptureQueriesContext(connection) as grand_queries:
            authenticated_client.get(_detail_url(organisme.id, grand.pk))

        assert len(grand_queries) == len(petit_queries)


@pytest.fixture(name="recrutement_liste")
def recrutement_liste_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR,
        utilisateur=test_user,
        id=UUID(ORGANISME_UUID),
    )
    offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
    return RecrutementDjangoFactory(organisme=organisme, offre=offer)


def _etapes_attendues(recrutement) -> list[dict]:
    etapes = {
        str(etape.id): etape
        for etape in EtapeModel.objects.filter(recrutement=recrutement)
    }
    return [
        {
            "uuid": etape_id,
            "nom": etapes[etape_id].nom,
            "categorie": CategorieEtapeRecrutement(etapes[etape_id].categorie).name,
        }
        for etape_id in recrutement.ordre_etapes
    ]


@pytest.mark.django_db
class TestRecrutementListeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_candidature_structure(self, authenticated_client, recrutement_liste):
        etape = EtapeModel.objects.get(
            recrutement=recrutement_liste,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        )
        candidature = CandidatureDjangoFactory(etape=etape)

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_200_OK
        dt = serializers.DateTimeField().to_representation
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "unread_conversations": 0,
                    "uuid": str(candidature.id),
                    "date_soumission": dt(candidature.created_at),
                    "candidat": {
                        "uuid": str(candidature.candidat_id),
                        "nom": candidature.candidat.utilisateur.last_name,
                        "prenom": candidature.candidat.utilisateur.first_name,
                    },
                    "date_derniere_activite": dt(candidature.updated_at),
                    "etape": {
                        "uuid": str(etape.id),
                        "nom": etape.nom,
                        "categorie": "ENTREE",
                    },
                }
            ],
            "etapes": _etapes_attendues(recrutement_liste),
        }

    def test_counts_unread_conversations_of_the_current_agent(
        self, authenticated_client, recrutement_liste, test_user
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        candidature = CandidatureDjangoFactory(etape=etape)
        ConversationDjangoFactory.create_batch(
            2,
            candidature=candidature,
            with_message=True,
            with_message__par_candidat=True,
        )
        answered = MessageDjangoFactory(
            conversation=ConversationDjangoFactory(candidature=candidature),
            auteur=test_user,
        )
        read = MessageDjangoFactory(
            conversation=ConversationDjangoFactory(candidature=candidature),
            par_candidat=True,
        )
        ConversationLectureDjangoFactory(
            conversation=read.conversation,
            utilisateur=test_user,
            read_at=read.created_at,
        )
        unread_by_another_agent_only = CandidatureDjangoFactory(etape=etape)
        ConversationDjangoFactory(
            candidature=unread_by_another_agent_only,
            with_message=True,
            with_message__par_candidat=True,
        )
        ConversationLectureDjangoFactory(
            conversation=answered.conversation,
            read_at=answered.created_at,
        )

        results = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["results"]

        assert {r["uuid"]: r["unread_conversations"] for r in results} == {
            str(candidature.id): 2,
            str(unread_by_another_agent_only.id): 1,
        }

    def test_returns_only_candidatures_of_the_recrutement(
        self, authenticated_client, recrutement_liste
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        candidature = CandidatureDjangoFactory(etape=etape)
        CandidatureDjangoFactory()

        data = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()

        assert data["count"] == 1
        assert [c["uuid"] for c in data["results"]] == [str(candidature.id)]

    @pytest.mark.parametrize(
        "role",
        [AgentRecrutementRole.CONTRIBUTEUR, AgentRecrutementRole.RECRUTEUR],
    )
    def test_membre_assigned_to_recrutement_is_allowed(
        self, authenticated_client, test_user, role
    ):
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            offre=OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID)),
            agent_link__agent=agent,
            agent_link__role=role.value,
        )
        etape = EtapeModel.objects.filter(recrutement=recrutement).first()
        candidature = CandidatureDjangoFactory(etape=etape)

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert [c["uuid"] for c in data["results"]] == [str(candidature.id)]
        assert data["etapes"] == _etapes_attendues(recrutement)

    def test_etapes_follow_the_order_of_the_recrutement(
        self, authenticated_client, recrutement_liste
    ):
        recrutement_liste.ordre_etapes = list(reversed(recrutement_liste.ordre_etapes))
        recrutement_liste.save(update_fields=["ordre_etapes"])

        etapes = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["etapes"]

        assert [e["uuid"] for e in etapes] == recrutement_liste.ordre_etapes

    def test_etapes_include_etapes_without_candidatures(
        self, authenticated_client, recrutement_liste
    ):
        data = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()

        assert data["results"] == []
        assert data["etapes"] == _etapes_attendues(recrutement_liste)
        assert data["etapes"]

    def test_etapes_are_returned_on_every_page(
        self, authenticated_client, recrutement_liste
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        CandidatureDjangoFactory.create_batch(NOMBRE_CANDIDATURES, etape=etape)

        with patch.object(TaillePageNumberPagination, "max_page_size", TAILLE_PAGE):
            premiere, seconde = (
                authenticated_client.get(
                    f"{RECRUTEMENT_LISTE_URL}?page={page}&taille={TAILLE_PAGE}"
                ).json()
                for page in (1, 2)
            )

        etapes = _etapes_attendues(recrutement_liste)
        assert premiere["etapes"] == seconde["etapes"] == etapes

    def test_candidature_order(self, authenticated_client, recrutement_liste):
        premiere_etape, seconde_etape = list(
            EtapeModel.objects.filter(recrutement=recrutement_liste)
        )[:2]
        maintenant = datetime.now(tz=timezone.utc)
        EtapeModel.objects.filter(pk=seconde_etape.pk).update(
            updated_at=maintenant - timedelta(days=2)
        )
        EtapeModel.objects.filter(pk=premiere_etape.pk).update(updated_at=maintenant)

        creee_maintenant = CandidatureDjangoFactory(etape=premiere_etape)
        creee_hier = CandidatureDjangoFactory(etape=premiere_etape)
        ancienne = CandidatureDjangoFactory(etape=seconde_etape)
        CandidatureModel.objects.filter(pk=creee_maintenant.pk).update(
            created_at=maintenant
        )
        CandidatureModel.objects.filter(pk=creee_hier.pk).update(
            created_at=maintenant - timedelta(days=1)
        )

        data = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()

        assert [c["uuid"] for c in data["results"]] == [
            str(ancienne.pk),
            str(creee_hier.pk),
            str(creee_maintenant.pk),
        ]

    def test_date_derniere_activite_prefers_recruteur_update(
        self, authenticated_client, recrutement_liste
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        mise_a_jour = datetime(2026, 1, 2, tzinfo=timezone.utc)
        CandidatureDjangoFactory(etape=etape, updated_by_recruteur=mise_a_jour)

        result = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["results"][0]

        assert datetime.fromisoformat(result["date_derniere_activite"]) == mise_a_jour

    @pytest.mark.parametrize(
        ("query", "max_page_size", "has_previous"),
        [
            pytest.param(f"?taille={TAILLE_PAGE}", None, False, id="first_page"),
            pytest.param(f"?page=2&taille={TAILLE_PAGE}", None, True, id="second_page"),
            pytest.param("?taille=50", TAILLE_PAGE, False, id="capped_to_max"),
        ],
    )
    def test_pagination_limits_page_size(
        self,
        authenticated_client,
        recrutement_liste,
        query,
        max_page_size,
        has_previous,
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        CandidatureDjangoFactory.create_batch(NOMBRE_CANDIDATURES, etape=etape)

        with patch.object(
            TaillePageNumberPagination,
            "max_page_size",
            max_page_size or TaillePageNumberPagination.max_page_size,
        ):
            data = authenticated_client.get(RECRUTEMENT_LISTE_URL + query).json()

        assert data["count"] == NOMBRE_CANDIDATURES
        assert len(data["results"]) == TAILLE_PAGE
        assert data["next"] is not None
        assert (data["previous"] is not None) is has_previous

    def test_unknown_page_returns_404(self, authenticated_client, recrutement_liste):
        response = authenticated_client.get(RECRUTEMENT_LISTE_URL + "?page=2")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        ("organisme_uuid", "recrutement_uuid"),
        [
            pytest.param(ORGANISME_UUID, UNKNOWN_RECRUTEMENT_UUID, id="recrutement"),
            pytest.param(UNKNOWN_RECRUTEMENT_UUID, RECRUTEMENT_UUID, id="organisme"),
        ],
    )
    def test_returns_404_for_unknown(
        self, authenticated_client, recrutement_liste, organisme_uuid, recrutement_uuid
    ):
        response = authenticated_client.get(
            reverse(
                "recruteur:organisme_recrutement_liste",
                kwargs={
                    "organisme_uuid": organisme_uuid,
                    "recrutement_uuid": recrutement_uuid,
                },
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_returns_403_when_not_authorized(self, authenticated_client):
        organisme = OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))
        RecrutementDjangoFactory(
            organisme=organisme, offre=OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        )

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}

    def test_returns_500_on_unexpected_error(
        self, authenticated_client, recrutement_liste
    ):
        with patch.object(
            OrganismePermissionService,
            "can_execute",
            side_effect=Exception("unexpected"),
        ):
            response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, recrutement_liste, django_assert_num_queries
    ):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        CandidatureDjangoFactory.create_batch(5, etape=etape)

        with django_assert_num_queries(NOMBRE_REQUETES_LISTE_ATTENDU):
            response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_200_OK


UNCHANGED_LIST_QUERY_COUNT = (
    2  # authentication (view + RateLimitHeadersMiddleware)
    + 1  # organisme
    + 1  # agent's role
    + 1  # version of the list
)


def _modify_candidature(recrutement, candidature, agent):
    candidature.updated_by_recruteur = datetime.now(timezone.utc)
    candidature.save()


def _change_etape(recrutement, candidature, agent):
    candidature.etape = EtapeModel.objects.filter(recrutement=recrutement).last()
    candidature.save()


def _add_candidature(recrutement, candidature, agent):
    CandidatureDjangoFactory(etape=candidature.etape)


def _delete_another_candidature(recrutement, candidature, agent):
    CandidatureModel.objects.exclude(pk=candidature.pk).delete()


def _rename_etape(recrutement, candidature, agent):
    etape = candidature.etape
    etape.nom = "Étape renommée"
    etape.save()


def _reorder_etapes(recrutement, candidature, agent):
    recrutement.ordre_etapes = list(reversed(recrutement.ordre_etapes))
    recrutement.save()


def _message_from_candidat(recrutement, candidature, agent):
    MessageDjangoFactory(
        conversation=ConversationDjangoFactory(candidature=candidature),
        par_candidat=True,
    )


def _read_by_current_agent(recrutement, candidature, agent):
    message = candidature.conversations.get().messages.get()
    mark_as_read(
        conversation_id=message.conversation_id,
        utilisateur=agent,
        read_up_to=message.created_at,
    )


@pytest.fixture(name="list_with_candidature")
def list_with_candidature_fixture(recrutement_liste):
    etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
    candidature = CandidatureDjangoFactory(etape=etape)
    CandidatureDjangoFactory(etape=etape)
    ConversationDjangoFactory(
        candidature=candidature, with_message=True, with_message__par_candidat=True
    )
    return recrutement_liste, candidature


@pytest.mark.django_db
class TestRecrutementListeConditionalGet:
    def test_returns_304_without_loading_the_list(
        self, authenticated_client, list_with_candidature, django_assert_num_queries
    ):
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        with django_assert_num_queries(UNCHANGED_LIST_QUERY_COUNT):
            second = authenticated_client.get(
                RECRUTEMENT_LISTE_URL, HTTP_IF_NONE_MATCH=first["ETag"]
            )

        assert second.status_code == status.HTTP_304_NOT_MODIFIED
        assert second.content == b""
        assert second["ETag"] == first["ETag"]
        assert set(second["Cache-Control"].split(", ")) == {"private", "no-cache"}

    @pytest.mark.parametrize(
        "change",
        [
            _modify_candidature,
            _change_etape,
            _add_candidature,
            _delete_another_candidature,
            _rename_etape,
            _reorder_etapes,
            _message_from_candidat,
            _read_by_current_agent,
        ],
    )
    def test_returns_200_after_a_change(
        self, authenticated_client, list_with_candidature, test_user, change
    ):
        recrutement, candidature = list_with_candidature
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        change(recrutement, candidature, test_user)
        second = authenticated_client.get(
            RECRUTEMENT_LISTE_URL, HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_200_OK
        assert second["ETag"] != first["ETag"]

    def test_reading_by_another_agent_keeps_the_list_unchanged(
        self, authenticated_client, list_with_candidature
    ):
        _, candidature = list_with_candidature
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        message = candidature.conversations.get().messages.get()
        ConversationLectureDjangoFactory(
            conversation=message.conversation, read_at=message.created_at
        )
        second = authenticated_client.get(
            RECRUTEMENT_LISTE_URL, HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_304_NOT_MODIFIED

    def test_etag_depends_on_the_query_string(
        self, authenticated_client, list_with_candidature
    ):
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        second = authenticated_client.get(
            RECRUTEMENT_LISTE_URL + "?taille=1", HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_200_OK

    def test_etag_depends_on_the_user(
        self, authenticated_client, list_with_candidature
    ):
        recrutement, _ = list_with_candidature
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        other = OrganismeAgentDjangoFactory(
            organisme=recrutement.organisme,
            role=AgentOrganismeRole.SUPERVISEUR.value,
        ).agent.utilisateur
        authenticated_client.force_login(other)

        second = authenticated_client.get(
            RECRUTEMENT_LISTE_URL, HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_200_OK

    def test_checks_permissions_before_answering_304(
        self, authenticated_client, list_with_candidature, test_user
    ):
        first = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        OrganismeAgentModel.objects.filter(agent_id=test_user.username).delete()

        second = authenticated_client.get(
            RECRUTEMENT_LISTE_URL, HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_403_FORBIDDEN


class TestRecrutementCandidaturesEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_echoes_candidatures_as_reussites(self, container, authenticated_client):
        candidatures = CandidatureRecruteurFactory.create_entity_batch(3)
        mock_usecase = container.change_etape_candidatures_usecase.return_value
        mock_usecase.execute.return_value = {
            "successes": candidatures,
            "failures": [],
        }

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={
                "etape_cible_uuid": fake.uuid4(),
                "candidatures": [
                    {
                        "candidature_uuid": str(c.entity_id),
                    }
                    for c in candidatures
                ],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reussites"] == [str(c.entity_id) for c in candidatures]
        assert data["echecs"] == []

    def test_requires_etape_cible_uuid(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        ("entity_id", "domain_error"),
        [
            pytest.param(
                ORGANISME_UUID,
                OrganismeNexistePas,
                id="organisme",
            ),
            pytest.param(
                RECRUTEMENT_UUID,
                RecrutementInexistant,
                id="recrutement",
            ),
            pytest.param(
                CANDIDATURE_UUID,
                CandidatureInexistante,
                id="candidature",
            ),
        ],
    )
    def test_returns_404_for_unknown(
        self, container, authenticated_client, entity_id, domain_error
    ):
        mock_usecase = container.change_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = domain_error(entity_id)

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": domain_error(entity_id).message}

    def test_returns_400_for_unknown_etape(self, container, authenticated_client):
        mock_usecase = container.change_etape_candidatures_usecase.return_value
        uuid = fake.uuid4()
        mock_usecase.execute.side_effect = RecrutementEtapeInexistante(
            uuid, RECRUTEMENT_UUID
        )

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": RecrutementEtapeInexistante(uuid, RECRUTEMENT_UUID).message
        }

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        mock_usecase = container.change_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = Exception("unexpected")

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    def test_rejects_unknown_motif_refus(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={
                "etape_cible_uuid": fake.uuid4(),
                "candidatures": [],
                "motif_refus": "not_a_real_motif",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_when_motif_refus_required(
        self, container, authenticated_client
    ):
        mock_usecase = container.change_etape_candidatures_usecase.return_value
        uuid = fake.uuid4()
        mock_usecase.execute.side_effect = MotifRefusRequis(uuid)

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": MotifRefusRequis(uuid).message}


class TestRecrutementCandidaturesEtapeViewDbVerified:
    def test_moves_candidature_and_persists_it(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offer)
        origine, cible = list(EtapeModel.objects.filter(recrutement=recrutement))[:2]
        candidature = CandidatureDjangoFactory(etape=origine)

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={
                "etape_cible_uuid": str(cible.id),
                "candidatures": [{"candidature_uuid": str(candidature.id)}],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reussites"] == [str(candidature.id)]
        assert data["echecs"] == []

        candidature.refresh_from_db()
        assert str(candidature.etape_id) == str(cible.id)
