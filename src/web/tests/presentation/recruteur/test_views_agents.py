from uuid import uuid4

from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

fake = Faker("fr_FR")

AGENTS_URL = reverse("recruteur:agents")


def _organisme_supervise_par(utilisateur):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=utilisateur
    )
    return organisme


def test_anonymous_access_is_unauthorized(api_client):
    response = api_client.post(AGENTS_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_creates_the_agent_and_logs_the_caller(authenticated_client, test_user):
    organisme = _organisme_supervise_par(test_user)
    email = fake.email()

    response = authenticated_client.post(
        AGENTS_URL, {"email": email, "organisme_id": str(organisme.id)}
    )

    assert response.status_code == status.HTTP_201_CREATED
    created = UserModel.objects.get(email=email)
    assert response.json() == {
        "uuid": str(created.username),
        "email": email,
        "prenom": "",
        "nom": "",
        "intitule_poste": "",
    }
    assert ProfilAgentModel.objects.filter(utilisateur=created).exists()
    [log] = AuditLogModel.objects.filter(ressource_kind="Agent")
    assert (log.event_name, log.utilisateur_id, log.ressource_id) == (
        "ProfilAgentCree",
        test_user.username,
        created.username,
    )


def test_reuses_an_existing_account_whatever_the_case(authenticated_client, test_user):
    organisme = _organisme_supervise_par(test_user)
    existing = UtilisateurDjangoFactory(
        email="marie.martin@gouv.fr", first_name="Marie", last_name="Martin"
    )

    response = authenticated_client.post(
        AGENTS_URL,
        {"email": "Marie.MARTIN@gouv.fr", "organisme_id": str(organisme.id)},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["uuid"] == str(existing.username)
    assert (response.json()["prenom"], response.json()["nom"]) == ("Marie", "Martin")
    assert UserModel.objects.filter(email="marie.martin@gouv.fr").count() == 1


def test_refuses_a_second_agent_profile(authenticated_client, test_user):
    organisme = _organisme_supervise_par(test_user)
    existing = AgentDjangoFactory()
    email = existing.utilisateur.email

    response = authenticated_client.post(
        AGENTS_URL, {"email": email, "organisme_id": str(organisme.id)}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error": str(ProfilAgentExisteDeja(email))}
    assert (
        ProfilAgentModel.objects.filter(utilisateur=existing.utilisateur).count() == 1
    )
    assert not AuditLogModel.objects.exists()


def test_missing_organisme_returns_bad_request(authenticated_client):
    response = authenticated_client.post(AGENTS_URL, {"email": fake.email()})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_refuses_a_caller_outside_the_organisme_and_writes_nothing(
    authenticated_client, test_user
):
    _organisme_supervise_par(test_user)
    other_organisme = OrganismeDjangoFactory()
    email = fake.email()

    response = authenticated_client.post(
        AGENTS_URL, {"email": email, "organisme_id": str(other_organisme.id)}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not UserModel.objects.filter(email=email).exists()
    assert not AuditLogModel.objects.exists()


def test_unknown_organisme_returns_not_found(authenticated_client, test_user):
    _organisme_supervise_par(test_user)

    response = authenticated_client.post(
        AGENTS_URL, {"email": fake.email(), "organisme_id": str(uuid4())}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "organisme_id: Not found."}
