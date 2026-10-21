import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)

URL = reverse("identite:user_details")

NOMBRE_REQUETES_ATTENDU = (
    1  # session
    + 1  # authentification : utilisateur de la session
    + 1  # service : rattachements actifs, organisme joint
    + 1  # service : organismes dont l'agent est responsable d'un recrutement
)


def _role(organisme, role: AgentOrganismeRole) -> dict:
    return {
        "organisme_uuid": str(organisme.id),
        "nom": organisme.nom,
        "role": role.value,
    }


def _organisme(organisme, role: AgentOrganismeRole, utilisateur) -> dict:
    return {
        "uuid": str(organisme.id),
        "nom": organisme.nom,
        "authorized_actions": [
            action.value
            for action in OrganismePermissionService().authorized_actions_organisme(
                role,
                utilisateur=utilisateur,
                organisme_id=organisme.id,
                organisme_ids_responsable=set(),
            )
        ],
    }


def test_anonymous_returns_401(api_client):
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "create_profil",
    [CandidatDjangoFactory, AgentDjangoFactory],
    ids=["candidat", "agent_sans_role"],
)
def test_user_without_organisme_role_has_no_organisme_roles(
    authenticated_client, test_user, create_profil
):
    create_profil(utilisateur=test_user)
    create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": test_user.email,
        "prenom": test_user.first_name,
        "nom": test_user.last_name,
        "is_staff": False,
        "organisme_roles": [],
        "authorized_actions": [],
        "organismes": [],
    }


@pytest.mark.parametrize(
    "has_candidate_profile", [True, False], ids=["avec_profil_candidat", "agent"]
)
def test_agent_with_role_has_organisme_roles(
    authenticated_client, test_user, has_candidate_profile
):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    if has_candidate_profile:
        CandidatDjangoFactory(utilisateur=test_user)

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": test_user.email,
        "prenom": test_user.first_name,
        "nom": test_user.last_name,
        "is_staff": False,
        "organisme_roles": [_role(organisme, AgentOrganismeRole.SUPERVISEUR)],
        "authorized_actions": [],
        "organismes": [
            _organisme(organisme, AgentOrganismeRole.SUPERVISEUR, test_user)
        ],
    }


def test_agent_with_multiple_roles(authenticated_client, test_user):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT,
        utilisateur=test_user,
        nom="Préfecture du Rhône",
    )
    other_organisme = OrganismeDjangoFactory(
        nom="Direction régionale des finances publiques"
    )
    OrganismeAgentDjangoFactory(
        organisme=other_organisme,
        agent=agent,
        role=AgentOrganismeRole.SUPERVISEUR.value,
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["organisme_roles"] == [
        _role(other_organisme, AgentOrganismeRole.SUPERVISEUR),
        _role(organisme, AgentOrganismeRole.AGENT),
    ]
    assert [o["uuid"] for o in response.json()["organismes"]] == [
        str(other_organisme.id),
        str(organisme.id),
    ]


def test_revoked_organisme_is_not_in_organisme_roles(authenticated_client, test_user):
    agent, organisme_actif = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    OrganismeAgentDjangoFactory(
        organisme=OrganismeDjangoFactory(),
        agent=agent,
        role=AgentOrganismeRole.SUPERVISEUR.value,
        date_revocation=timezone.now(),
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["organisme_roles"] == [
        _role(organisme_actif, AgentOrganismeRole.AGENT)
    ]
    assert response.json()["organismes"] == [
        _organisme(organisme_actif, AgentOrganismeRole.AGENT, test_user)
    ]


def test_supprime_organisme_is_not_in_organisme_roles(authenticated_client, test_user):
    agent, organisme_actif = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    OrganismeAgentDjangoFactory(
        organisme=OrganismeDjangoFactory(supprime_le=timezone.now()),
        agent=agent,
        role=AgentOrganismeRole.SUPERVISEUR.value,
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["organisme_roles"] == [
        _role(organisme_actif, AgentOrganismeRole.AGENT)
    ]
    assert response.json()["organismes"] == [
        _organisme(organisme_actif, AgentOrganismeRole.AGENT, test_user)
    ]


def test_returns_staff_flag(authenticated_client, test_user):
    test_user.is_staff = True
    test_user.save()

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_staff"] is True


def test_staff_has_staff_and_superviseur_actions(authenticated_client, test_user):
    test_user.is_staff = True
    test_user.save()
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["authorized_actions"] == [
        "create_organisme",
        "list_organismes",
        "update_organisme",
    ]
    assert body["organismes"] == [
        _organisme(organisme, AgentOrganismeRole.AGENT, test_user)
    ]
    assert "get_organisme" in body["organismes"][0]["authorized_actions"]


def test_agent_authorized_actions_exclude_recrutement_level(
    authenticated_client, test_user
):
    create_organisme_with_agent(role=AgentOrganismeRole.AGENT, utilisateur=test_user)

    response = authenticated_client.get(URL)

    assert response.json()["organismes"][0]["authorized_actions"] == [
        "list_recrutements",
        "get_motifs_refus",
    ]


def test_responsable_agent_gets_search_and_create_agent_in_its_organisme_only(
    authenticated_client, test_user
):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    other_organisme = OrganismeDjangoFactory(nom="Zzz")
    OrganismeAgentDjangoFactory(
        organisme=other_organisme, agent=agent, role=AgentOrganismeRole.AGENT.value
    )
    RecrutementAgentDjangoFactory(
        recrutement=RecrutementDjangoFactory(organisme=organisme),
        agent=agent,
        role=AgentRecrutementRole.RESPONSABLE.value,
    )

    response = authenticated_client.get(URL)

    actions_by_uuid = {
        o["uuid"]: o["authorized_actions"] for o in response.json()["organismes"]
    }
    assert "search_agent" in actions_by_uuid[str(organisme.id)]
    assert "create_agent" in actions_by_uuid[str(organisme.id)]
    assert "search_agent" not in actions_by_uuid[str(other_organisme.id)]
    assert "create_agent" not in actions_by_uuid[str(other_organisme.id)]


@pytest.mark.parametrize(
    ("role", "revoquee"),
    [
        (AgentRecrutementRole.RECRUTEUR, False),
        (AgentRecrutementRole.CONTRIBUTEUR, False),
        (AgentRecrutementRole.RESPONSABLE, True),
    ],
    ids=["recruteur", "contributeur", "responsable_revoque"],
)
def test_agent_not_responsable_of_a_recrutement_gets_no_agent_management_actions(
    authenticated_client, test_user, role, revoquee
):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    RecrutementAgentDjangoFactory(
        recrutement=RecrutementDjangoFactory(organisme=organisme),
        agent=agent,
        role=role.value,
        date_revocation=timezone.now() if revoquee else None,
    )

    response = authenticated_client.get(URL)

    assert response.json()["organismes"][0]["authorized_actions"] == [
        "list_recrutements",
        "get_motifs_refus",
    ]


def test_does_not_query_organisme_per_role(
    authenticated_client, test_user, django_assert_num_queries
):
    agent, organisme = create_organisme_with_agent(utilisateur=test_user)
    other_organisme = OrganismeDjangoFactory()
    OrganismeAgentDjangoFactory(organisme=other_organisme, agent=agent)
    for responsable_de in (organisme, other_organisme):
        RecrutementAgentDjangoFactory(
            recrutement=RecrutementDjangoFactory(organisme=responsable_de),
            agent=agent,
            role=AgentRecrutementRole.RESPONSABLE.value,
        )

    with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
        response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert {r["organisme_uuid"] for r in response.json()["organisme_roles"]} == {
        str(organisme.id),
        str(other_organisme.id),
    }
