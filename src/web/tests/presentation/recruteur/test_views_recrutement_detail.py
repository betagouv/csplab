from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from faker import Faker
from rest_framework import serializers, status

from application.recruteur.dtos.recrutement_read_models import (
    CandidatDto,
    CandidatureKanbanDto,
    EtapeKanbanReadModel,
    RecrutementKanbanReadModel,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
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
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
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


def _recrutement_kanban_read_model() -> RecrutementKanbanReadModel:
    return RecrutementKanbanReadModel(
        offer_id=UUID(RECRUTEMENT_UUID),
        etapes=[
            EtapeKanbanReadModel(
                etape_uuid=uuid4(),
                nom="Réception des candidatures",
                categorie="ENTREE",
                candidatures=[
                    CandidatureKanbanDto(
                        uuid=uuid4(),
                        date_soumission=datetime.now(tz=timezone.utc),
                        date_derniere_activite=datetime.now(tz=timezone.utc),
                        candidat=CandidatDto(
                            uuid=uuid4(), nom="Dupont", prenom="Alice"
                        ),
                    )
                ],
            ),
            EtapeKanbanReadModel(
                etape_uuid=uuid4(),
                nom="Candidature acceptée",
                categorie="ACCEPTE",
                candidatures=[],
            ),
        ],
    )


ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"
UNKNOWN_RECRUTEMENT_UUID = fake.uuid4()

CANDIDATURE_UUID = "aaaaaaaa-0002-0002-0002-000000000002"

RECRUTEMENT_CANDIDATURES_ETAPE_URL = reverse(
    "recruteur:organisme_recrutement_candidatures_etape",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_KANBAN_URL = reverse(
    "recruteur:organisme_recrutement_kanban",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_LISTE_URL = reverse(
    "recruteur:organisme_recrutement_liste",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
UNKNOWN_RECRUTEMENT_KANBAN_URL = reverse(
    "recruteur:organisme_recrutement_kanban",
    kwargs={
        "organisme_uuid": ORGANISME_UUID,
        "recrutement_uuid": UNKNOWN_RECRUTEMENT_UUID,
    },
)
RECRUTEMENT_DETAIL_URL = reverse(
    "recruteur:organisme_recrutement",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)

NOMBRE_REQUETES_LISTE_ATTENDU = (
    2  # authentication (view + RateLimitHeadersMiddleware)
    + 1  # organisme
    + 1  # agent's role
    + 1  # recrutement belongs to organisme (exists check)
    + 2  # pagination: count + page
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


class TestRecrutementDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_detail_payload(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        offre = OfferDjangoFactory(title="Chargé de mission numérique", category="A")
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        payload = response.json()
        assert set(payload) == {
            "uuid",
            "intitule",
            "archive",
            "date_publication",
            "localisation",
            "organisme_recruteur",
            "categorie_offre",
            "etapes",
            "recrutement_role",
        }
        assert payload["recrutement_role"] is None
        assert payload["uuid"] == str(recrutement.pk)
        assert payload["intitule"] == "Chargé de mission numérique"
        assert payload["archive"] is False
        assert payload["categorie_offre"] == "A"
        assert payload["organisme_recruteur"] == {
            "nom": organisme.nom,
            "siret": organisme.siret,
        }
        assert set(payload["localisation"]) == {
            "zone_geographique",
            "pays",
            "region",
            "departement",
            "localisation_label",
            "latitude",
            "longitude",
        }

    def test_localisation_with_nullable_offre_columns(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        offre = OfferDjangoFactory(
            area=None,
            country=None,
            region=None,
            department=None,
            location_label=None,
            latitude=None,
            longitude=None,
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

        response = authenticated_client.get(_detail_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["localisation"] == {
            "zone_geographique": "",
            "pays": "",
            "region": "",
            "departement": "",
            "localisation_label": "",
            "latitude": None,
            "longitude": None,
        }

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

    def test_staff_gets_detail_without_organisme_role(self, api_client):
        api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
        recrutement = RecrutementDjangoFactory()

        response = api_client.get(_detail_url(recrutement.organisme_id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK

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


class TestRecrutementKanbanView:
    @pytest.fixture(autouse=True)
    def _default_usecase(self, container):
        container.get_recrutement_kanban_usecase.return_value.execute.return_value = (
            _recrutement_kanban_read_model()
        )

    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_response_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        assert set(data) == {"uuid", "etapes"}
        assert isinstance(data["etapes"], list)

    def test_etape_structure(self, authenticated_client):
        etape = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()["etapes"][0]
        assert "uuid" in etape
        assert "nom" in etape
        assert "categorie" in etape
        assert "candidatures" in etape
        assert isinstance(etape["candidatures"], list)

    def test_candidature_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        candidature = data["etapes"][0]["candidatures"][0]
        assert "uuid" in candidature
        assert "date_soumission" in candidature
        assert "candidat" in candidature
        assert "uuid" in candidature["candidat"]
        assert "nom" in candidature["candidat"]
        assert "prenom" in candidature["candidat"]

    def test_etapes_order(self, authenticated_client):
        etapes = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()["etapes"]
        assert etapes[0]["categorie"] == "ENTREE"
        assert etapes[-1]["categorie"] == "ACCEPTE"

    def test_etape_accepte_has_no_candidatures(self, authenticated_client):
        etape_accepte = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()[
            "etapes"
        ][-1]
        assert etape_accepte["categorie"] == "ACCEPTE"
        assert etape_accepte["candidatures"] == []

    def test_returns_404_for_unknown_recrutement(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.return_value = (
            None
        )

        response = authenticated_client.get(UNKNOWN_RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_returns_403_when_not_authorized(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(UUID(fake.uuid4()))
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


@pytest.fixture(name="recrutement_liste")
def recrutement_liste_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR,
        utilisateur=test_user,
        id=UUID(ORGANISME_UUID),
    )
    offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
    return RecrutementDjangoFactory(organisme=organisme, offre=offer)


@pytest.mark.django_db
class TestRecrutementListeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_candidature_structure(self, authenticated_client, recrutement_liste):
        etape = EtapeModel.objects.filter(recrutement=recrutement_liste).first()
        candidature = CandidatureDjangoFactory(etape=etape)
        candidature.refresh_from_db()

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

    def test_membre_assigned_to_recrutement_is_allowed(
        self, authenticated_client, test_user
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
        )
        etape = EtapeModel.objects.filter(recrutement=recrutement).first()
        candidature = CandidatureDjangoFactory(etape=etape)

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [c["uuid"] for c in response.json()["results"]] == [str(candidature.id)]

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
        with patch(
            "presentation.recruteur.views.recrutement_detail.list_candidatures",
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
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
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
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = domain_error(entity_id)

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": domain_error(entity_id).message}

    def test_returns_400_for_unknown_etape(self, container, authenticated_client):
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
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
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
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
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        uuid = fake.uuid4()
        mock_usecase.execute.side_effect = MotifRefusRequis(uuid)

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": MotifRefusRequis(uuid).message}


class TestRecrutementKanbanViewDbVerified:
    def test_returns_persisted_kanban(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offer)

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["uuid"] == str(recrutement.offre_id)
        assert len(data["etapes"]) == len(recrutement.ordre_etapes)
        assert data["etapes"][0]["candidatures"] == []


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
