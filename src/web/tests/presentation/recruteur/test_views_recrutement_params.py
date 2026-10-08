from functools import partial
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status

from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    RecrutementEtapeIncoherents,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

fake = Faker()

ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"

RECRUTEMENT_ETAPES_URL = reverse(
    "recruteur:organisme_recrutement_etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_ETAPES_INIT_URL = reverse(
    "recruteur:organisme_recrutement_etapes_init",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)

RECRUTEMENT_KANBAN_URL = reverse(
    "recruteur:organisme_recrutement_kanban",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)

ETAPE_UUID = "aaaaaaaa-0002-0002-0002-000000000002"


def _etapes_payload(etapes) -> list[dict]:
    return [
        {"uuid": str(e.entity_id), "nom": e.nom, "categorie": e.categorie.name}
        for e in etapes
    ]


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_params.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized_on_get(self, api_client):
        response = api_client.get(RECRUTEMENT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_access_is_unauthorized_on_patch(self, api_client):
        response = api_client.patch(RECRUTEMENT_ETAPES_URL, data=[], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_requires_valid_body(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_201_with_updated_pipeline(self, container, authenticated_client):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        usecase = container.update_recrutement_etapes_usecase.return_value.execute
        usecase.return_value = etapes

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=_etapes_payload(etapes),
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(etapes)
        assert data[-1]["uuid"] == str(etapes[-1].entity_id)
        assert data[-1]["nom"] == "Recrutement"
        assert data[-1]["categorie"] == "ACCEPTE"
        (command,), _ = usecase.call_args
        assert [e.etape_uuid for e in command.etapes_data] == [
            e.entity_id for e in etapes
        ]

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeRecrutementIncoherents(
                    UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": OrganismeRecrutementIncoherents(
                        UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                    ).message
                },
            ),
            (
                RecrutementEtapeIncoherents(
                    recrutement_id=UUID(ORGANISME_UUID), etape_id=UUID(ETAPE_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": f"L'étape {ETAPE_UUID} ne correspond pas au recrutement"
                    f" {ORGANISME_UUID}"
                },
            ),
            (
                ConfigurationEtapesInvalide(
                    "La première étape doit être de catégorie ENTREE"
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": ConfigurationEtapesInvalide(
                        "La première étape doit être de catégorie ENTREE"
                    ).message
                },
            ),
            (
                SupressionEtapeImpossible(UUID(ETAPE_UUID), 1),
                status.HTTP_400_BAD_REQUEST,
                {"error": SupressionEtapeImpossible(UUID(ETAPE_UUID), 1).message},
            ),
            (
                AccesOrganismeRefuse(UUID(ORGANISME_UUID)),
                status.HTTP_403_FORBIDDEN,
                {"error": AccesOrganismeRefuse(UUID(ORGANISME_UUID)).message},
            ),
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                RecrutementInexistant(UUID(RECRUTEMENT_UUID)),
                status.HTTP_404_NOT_FOUND,
                {"error": RecrutementInexistant(UUID(RECRUTEMENT_UUID)).message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_patch_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        container.update_recrutement_etapes_usecase.return_value.execute.side_effect = (
            exception
        )
        etapes = EtapeRecrutementFactory.create_entity_batch()
        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=_etapes_payload(etapes),
            format="json",
        )

        assert response.status_code == expected_status
        assert response.json() == expected_body


def _etapes_url(organisme_id, recrutement_id):
    return reverse(
        "recruteur:organisme_recrutement_etapes",
        kwargs={"organisme_uuid": organisme_id, "recrutement_uuid": recrutement_id},
    )


def _init_url(organisme_id, recrutement_id):
    return reverse(
        "recruteur:organisme_recrutement_etapes_init",
        kwargs={"organisme_uuid": organisme_id, "recrutement_uuid": recrutement_id},
    )


def _recrutement_with_etapes(organisme, **kwargs):
    recrutement = RecrutementDjangoFactory(organisme=organisme, etapes=[], **kwargs)
    reception = EtapeDjangoFactory(
        recrutement=recrutement, nom="Réception", categorie="entree"
    )
    entretien = EtapeDjangoFactory(
        recrutement=recrutement, nom="Entretien", categorie="en_cours"
    )
    refus = EtapeDjangoFactory(recrutement=recrutement, nom="Refus", categorie="refus")
    recrutement.ordre_etapes = [str(e.id) for e in (reception, entretien, refus)]
    recrutement.save(update_fields=["ordre_etapes"])
    return recrutement, reception, entretien, refus


def _superviseur_recrutement(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    return organisme, *_recrutement_with_etapes(organisme)


class TestGetRecrutementEtapesView:
    def test_superviseur_gets_etapes_in_ordre(self, authenticated_client, test_user):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"uuid": str(reception.id), "nom": "Réception", "categorie": "ENTREE"},
            {"uuid": str(entretien.id), "nom": "Entretien", "categorie": "EN_COURS"},
            {"uuid": str(refus.id), "nom": "Refus", "categorie": "REFUS"},
        ]

    def test_etapes_follow_ordre_etapes(self, authenticated_client, test_user):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )
        recrutement.ordre_etapes = [str(e.id) for e in (refus, reception, entretien)]
        recrutement.save(update_fields=["ordre_etapes"])

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert [e["uuid"] for e in response.json()] == [
            str(refus.id),
            str(reception.id),
            str(entretien.id),
        ]

    def test_etape_missing_from_ordre_etapes_is_excluded(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )
        recrutement.ordre_etapes = [str(reception.id), str(refus.id)]
        recrutement.save(update_fields=["ordre_etapes"])

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert [e["uuid"] for e in response.json()] == [
            str(reception.id),
            str(refus.id),
        ]

    def test_agent_responsable_gets_etapes(self, authenticated_client, test_user):
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT, utilisateur=test_user
        )
        recrutement, reception, entretien, refus = _recrutement_with_etapes(
            organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert [e["uuid"] for e in response.json()] == [
            str(reception.id),
            str(entretien.id),
            str(refus.id),
        ]

    def test_staff_without_liaison_gets_etapes(self, api_client):
        api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            UtilisateurDjangoFactory()
        )

        response = api_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        assert [e["uuid"] for e in response.json()] == [
            str(reception.id),
            str(entretien.id),
            str(refus.id),
        ]

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR],
    )
    def test_agent_with_lower_recrutement_role_is_forbidden(
        self, authenticated_client, test_user, recrutement_role
    ):
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT, utilisateur=test_user
        )
        recrutement, *_ = _recrutement_with_etapes(
            organisme, agent_link__agent=agent, agent_link__role=recrutement_role.value
        )

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "error": AccesRecrutementRefuse(recrutement.pk).message
        }

    def test_agent_without_recrutement_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT, utilisateur=test_user
        )
        recrutement, *_ = _recrutement_with_etapes(organisme)

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "error": AccesRecrutementRefuse(recrutement.pk).message
        }

    def test_superviseur_of_another_organisme_is_forbidden(
        self, authenticated_client, test_user
    ):
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        _, autre_organisme = create_organisme_with_agent()
        recrutement, *_ = _recrutement_with_etapes(autre_organisme)

        response = authenticated_client.get(
            _etapes_url(autre_organisme.id, recrutement.pk)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "error": AccesOrganismeRefuse(autre_organisme.id).message
        }

    def test_non_member_is_forbidden_before_recrutement_lookup(
        self, authenticated_client
    ):
        _, organisme = create_organisme_with_agent()

        response = authenticated_client.get(_etapes_url(organisme.id, uuid4()))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": AccesOrganismeRefuse(organisme.id).message}

    def test_unknown_organisme_returns_404(self, authenticated_client):
        organisme_id = uuid4()

        response = authenticated_client.get(_etapes_url(organisme_id, uuid4()))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "error": OrganismeNexistePas(str(organisme_id)).message
        }

    def test_unknown_recrutement_returns_404(self, authenticated_client, test_user):
        organisme, *_ = _superviseur_recrutement(test_user)
        recrutement_id = uuid4()

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement_id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "error": RecrutementInexistant(recrutement_id).message
        }

    def test_recrutement_of_supprime_organisme_returns_404(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, *_ = _superviseur_recrutement(test_user)
        organisme.supprime_le = timezone.now()
        organisme.save(update_fields=["supprime_le"])

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "error": OrganismeNexistePas(str(organisme.id)).message
        }

    def test_recrutement_of_another_supprime_organisme_returns_404(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        _, autre_organisme = create_organisme_with_agent(supprime_le=timezone.now())
        recrutement, *_ = _recrutement_with_etapes(autre_organisme)

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "error": RecrutementInexistant(recrutement.pk).message
        }

    def test_recrutement_of_another_organisme_is_a_bad_request(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        _, autre_organisme = create_organisme_with_agent()
        recrutement, *_ = _recrutement_with_etapes(autre_organisme)

        response = authenticated_client.get(_etapes_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": OrganismeRecrutementIncoherents(
                organisme.id, recrutement.pk
            ).message
        }


class TestRecrutementEtapeViewDbVerified:
    def test_patch_persists_the_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        RecrutementDjangoFactory(organisme=organisme, offre=offer)
        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL, data=payload, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert [{"nom": e["nom"], "categorie": e["categorie"]} for e in data] == payload

        recrutement_model = RecrutementModel.objects.get(
            offre_id=UUID(RECRUTEMENT_UUID)
        )
        etapes_par_id = {str(e.id): e.nom for e in recrutement_model.etapes.all()}
        assert [etapes_par_id[i] for i in recrutement_model.ordre_etapes] == [
            e["nom"] for e in payload
        ]

    def test_kanban_reflects_the_patched_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        RecrutementDjangoFactory(organisme=organisme, offre=offer)
        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]
        authenticated_client.patch(RECRUTEMENT_ETAPES_URL, data=payload, format="json")

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [e["nom"] for e in response.json()["etapes"]] == [
            e["nom"] for e in payload
        ]


def _avec_etapes_organisme(organisme):
    organisme.etapes = [
        {"entity_id": str(uuid4()), "categorie": "entree", "nom": "Accueil"},
        {"entity_id": str(uuid4()), "categorie": "accepte", "nom": "Recrutement"},
    ]
    organisme.save(update_fields=["etapes"])
    return organisme


def _superviseur(test_user):
    organisme, recrutement, *anciennes_etapes = _superviseur_recrutement(test_user)
    return organisme, recrutement, anciennes_etapes


def _agent_responsable(test_user):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement, *anciennes_etapes = _recrutement_with_etapes(
        organisme,
        agent_link__agent=agent,
        agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
    )
    return organisme, recrutement, anciennes_etapes


def _staff_without_liaison(test_user):
    test_user.is_staff = True
    test_user.save(update_fields=["is_staff"])
    return _superviseur(UtilisateurDjangoFactory())


def _agent_with_recrutement_role(recrutement_role, test_user):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement, *_ = _recrutement_with_etapes(
        organisme, agent_link__agent=agent, agent_link__role=recrutement_role.value
    )
    return organisme.id, recrutement.pk, AccesRecrutementRefuse(recrutement.pk)


def _agent_without_recrutement_role(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement, *_ = _recrutement_with_etapes(organisme)
    return organisme.id, recrutement.pk, AccesRecrutementRefuse(recrutement.pk)


def _agent_on_unknown_recrutement(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement_id = uuid4()
    return organisme.id, recrutement_id, AccesRecrutementRefuse(recrutement_id)


def _agent_on_another_organisme(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    _, autre_organisme = create_organisme_with_agent()
    recrutement, *_ = _recrutement_with_etapes(autre_organisme)
    return organisme.id, recrutement.pk, AccesRecrutementRefuse(recrutement.pk)


def _superviseur_of_another_organisme(test_user):
    create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    _, autre_organisme = create_organisme_with_agent()
    recrutement, *_ = _recrutement_with_etapes(autre_organisme)
    return autre_organisme.id, recrutement.pk, AccesOrganismeRefuse(autre_organisme.id)


def _non_member(test_user):
    _, organisme = create_organisme_with_agent()
    return organisme.id, uuid4(), AccesOrganismeRefuse(organisme.id)


def _non_member_on_another_organisme(test_user):
    _, organisme = create_organisme_with_agent()
    _, autre_organisme = create_organisme_with_agent()
    recrutement, *_ = _recrutement_with_etapes(autre_organisme)
    return organisme.id, recrutement.pk, AccesOrganismeRefuse(organisme.id)


def _unknown_organisme(test_user):
    organisme_id = uuid4()
    return organisme_id, uuid4(), OrganismeNexistePas(str(organisme_id))


def _unknown_recrutement(test_user):
    organisme, *_ = _superviseur_recrutement(test_user)
    recrutement_id = uuid4()
    return organisme.id, recrutement_id, RecrutementInexistant(recrutement_id)


def _recrutement_of_supprime_organisme(test_user):
    organisme, recrutement, *_ = _superviseur_recrutement(test_user)
    organisme.supprime_le = timezone.now()
    organisme.save(update_fields=["supprime_le"])
    return organisme.id, recrutement.pk, OrganismeNexistePas(str(organisme.id))


def _recrutement_of_another_supprime_organisme(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    _, autre_organisme = create_organisme_with_agent(supprime_le=timezone.now())
    recrutement, *_ = _recrutement_with_etapes(autre_organisme)
    return organisme.id, recrutement.pk, RecrutementInexistant(recrutement.pk)


def _recrutement_of_another_organisme(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    _, autre_organisme = create_organisme_with_agent()
    recrutement, *_ = _recrutement_with_etapes(autre_organisme)
    return organisme.id, recrutement.pk, RecrutementInexistant(recrutement.pk)


class TestInitRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "arrange",
        [
            pytest.param(_superviseur, id="superviseur"),
            pytest.param(_agent_responsable, id="agent_responsable"),
            pytest.param(_staff_without_liaison, id="staff_without_liaison"),
        ],
    )
    def test_resets_etapes(self, authenticated_client, test_user, arrange):
        organisme, recrutement, anciennes_etapes = arrange(test_user)
        _avec_etapes_organisme(organisme)
        updated_at_avant = recrutement.updated_at

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert [(e["nom"], e["categorie"]) for e in data] == [
            ("Accueil", "ENTREE"),
            ("Recrutement", "ACCEPTE"),
        ]
        recrutement.refresh_from_db()
        assert recrutement.ordre_etapes == [e["uuid"] for e in data]
        assert sorted(str(e.id) for e in recrutement.etapes.all()) == sorted(
            e["uuid"] for e in data
        )
        assert not EtapeModel.objects.filter(
            id__in=[e.id for e in anciennes_etapes]
        ).exists()
        assert recrutement.updated_at > updated_at_avant

    @pytest.mark.parametrize(
        "arrange",
        [
            pytest.param(
                partial(_agent_with_recrutement_role, AgentRecrutementRole.RECRUTEUR),
                id="recruteur",
            ),
            pytest.param(
                partial(
                    _agent_with_recrutement_role, AgentRecrutementRole.CONTRIBUTEUR
                ),
                id="contributeur",
            ),
            pytest.param(
                _agent_without_recrutement_role, id="agent_without_recrutement_role"
            ),
            pytest.param(
                _agent_on_unknown_recrutement, id="agent_on_unknown_recrutement"
            ),
            pytest.param(_agent_on_another_organisme, id="agent_on_another_organisme"),
            pytest.param(
                _superviseur_of_another_organisme,
                id="superviseur_of_another_organisme",
            ),
            pytest.param(_non_member, id="non_member"),
            pytest.param(
                _non_member_on_another_organisme,
                id="non_member_on_another_organisme",
            ),
        ],
    )
    def test_is_forbidden(self, authenticated_client, test_user, arrange):
        organisme_id, recrutement_id, erreur = arrange(test_user)

        response = authenticated_client.post(_init_url(organisme_id, recrutement_id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": erreur.message}

    @pytest.mark.parametrize(
        "arrange",
        [
            pytest.param(_unknown_organisme, id="unknown_organisme"),
            pytest.param(_unknown_recrutement, id="unknown_recrutement"),
            pytest.param(
                _recrutement_of_supprime_organisme,
                id="recrutement_of_supprime_organisme",
            ),
            pytest.param(
                _recrutement_of_another_supprime_organisme,
                id="recrutement_of_another_supprime_organisme",
            ),
            pytest.param(
                _recrutement_of_another_organisme,
                id="recrutement_of_another_organisme",
            ),
        ],
    )
    def test_returns_404(self, authenticated_client, test_user, arrange):
        organisme_id, recrutement_id, erreur = arrange(test_user)

        response = authenticated_client.post(_init_url(organisme_id, recrutement_id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": erreur.message}

    def test_etape_with_candidatures_is_a_bad_request(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )
        _avec_etapes_organisme(organisme)
        CandidatureDjangoFactory(etape=entretien)
        CandidatureDjangoFactory(etape=entretien)
        ordre_avant = recrutement.ordre_etapes

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": SupressionEtapeImpossible(entretien.id, 2).message
        }
        recrutement.refresh_from_db()
        assert recrutement.ordre_etapes == ordre_avant
        assert sorted(e.id for e in recrutement.etapes.all()) == sorted(
            [reception.id, entretien.id, refus.id]
        )

    def test_etape_missing_from_ordre_etapes_is_kept(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, *_ = _superviseur_recrutement(test_user)
        _avec_etapes_organisme(organisme)
        orpheline = EtapeDjangoFactory(
            recrutement=recrutement, nom="Orpheline", categorie="en_cours"
        )

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_201_CREATED
        assert EtapeModel.objects.filter(id=orpheline.id).exists()
        assert str(orpheline.id) not in [e["uuid"] for e in response.json()]

    def test_organisme_without_etapes_leaves_recrutement_empty(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, *_ = _superviseur_recrutement(test_user)
        organisme.etapes = None
        organisme.save(update_fields=["etapes"])

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == []
        recrutement.refresh_from_db()
        assert recrutement.ordre_etapes == []
        assert not recrutement.etapes.exists()

    def test_unknown_organisme_categorie_rolls_back(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )
        organisme.etapes = [
            {"entity_id": str(uuid4()), "categorie": "inconnue", "nom": "Accueil"},
        ]
        organisme.save(update_fields=["etapes"])
        ordre_avant = recrutement.ordre_etapes

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
        recrutement.refresh_from_db()
        assert recrutement.ordre_etapes == ordre_avant
        assert sorted(e.id for e in recrutement.etapes.all()) == sorted(
            [reception.id, entretien.id, refus.id]
        )
        assert not AuditLogModel.objects.exists()

    def test_post_logs_deleted_added_and_reinitialized(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, reception, entretien, refus = _superviseur_recrutement(
            test_user
        )
        _avec_etapes_organisme(organisme)

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_201_CREATED
        entries = AuditLogModel.objects.values_list(
            "ressource_kind", "ressource_id", "event_name", "utilisateur_id"
        )
        expected = [
            ("EtapeRecrutement", etape.id, "EtapeSupprimee", test_user.username)
            for etape in (reception, entretien, refus)
        ]
        expected += [
            ("EtapeRecrutement", UUID(e["uuid"]), "EtapeAjoutee", test_user.username)
            for e in response.json()
        ]
        expected.append(
            (
                "Recrutement",
                recrutement.pk,
                "RecrutementEtapesReinitialisees",
                test_user.username,
            )
        )
        assert sorted(entries, key=str) == sorted(expected, key=str)

    def test_forbidden_post_logs_nothing(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT, utilisateur=test_user
        )
        recrutement, *_ = _recrutement_with_etapes(organisme)

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not AuditLogModel.objects.exists()

    def test_bad_request_post_logs_nothing(self, authenticated_client, test_user):
        organisme, recrutement, reception, *_ = _superviseur_recrutement(test_user)
        CandidatureDjangoFactory(etape=reception)

        response = authenticated_client.post(_init_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not AuditLogModel.objects.exists()
