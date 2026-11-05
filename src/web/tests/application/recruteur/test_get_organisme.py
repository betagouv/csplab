from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.get_organisme import get_organisme
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _supprime(organisme):
    organisme.supprime_le = datetime.now(timezone.utc)
    organisme.save(update_fields=["supprime_le"])


def test_returns_the_requested_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    OrganismeDjangoFactory()

    result = get_organisme(organisme_id=organisme.id, utilisateur=agent.utilisateur)

    assert result == organisme


def test_refuses_an_agent_without_the_required_role():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

    with pytest.raises(AccesOrganismeRefuse):
        get_organisme(organisme_id=organisme.id, utilisateur=agent.utilisateur)


def test_raises_when_organisme_is_supprime():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    _supprime(organisme)

    with pytest.raises(OrganismeNexistePas) as raised:
        get_organisme(organisme_id=organisme.id, utilisateur=agent.utilisateur)

    assert raised.value.identifier == str(organisme.id)


def test_raises_when_organisme_is_supprime_after_permission_check():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    _supprime(organisme)

    with patch.object(OrganismePermissionService, "can_execute"):
        with pytest.raises(OrganismeNexistePas) as raised:
            get_organisme(organisme_id=organisme.id, utilisateur=agent.utilisateur)

    assert raised.value.identifier == str(organisme.id)


def test_exposes_the_actions_of_a_superviseur():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    resultat = get_organisme(organisme_id=organisme.id, utilisateur=agent.utilisateur)

    actions = resultat.authorized_actions  # type: ignore[attr-defined]
    assert {"get_organisme", "attach_organisme_agent", "update_organisme_steps"} <= set(
        actions
    )


def test_staff_gets_the_actions_of_a_superviseur_without_liaison():
    organisme = OrganismeDjangoFactory()
    staff = UtilisateurDjangoFactory(is_staff=True)

    resultat = get_organisme(organisme_id=organisme.id, utilisateur=staff)

    assert resultat == organisme
    assert "get_organisme" in resultat.authorized_actions  # type: ignore[attr-defined]
