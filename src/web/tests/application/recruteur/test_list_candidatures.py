from uuid import uuid4

import pytest

from application.recruteur.services.list_candidatures import list_candidatures
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _agent_without_role_in_organisme():
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent, organisme.id, recrutement.pk


def _membre_not_assigned_to_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    return agent, organisme.id, recrutement.pk


def _superviseur_on_unknown_organisme():
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent, uuid4(), uuid4()


def _superviseur_on_recrutement_of_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent, organisme.id, RecrutementDjangoFactory().pk


@pytest.mark.parametrize(
    ("scenario", "expected_error"),
    [
        pytest.param(
            _agent_without_role_in_organisme,
            AccesOrganismeRefuse,
            id="no_role_in_organisme",
        ),
        pytest.param(
            _membre_not_assigned_to_recrutement,
            AccesRecrutementRefuse,
            id="membre_not_assigned",
        ),
        pytest.param(
            _superviseur_on_unknown_organisme,
            OrganismeNexistePas,
            id="unknown_organisme",
        ),
        pytest.param(
            _superviseur_on_recrutement_of_another_organisme,
            RecrutementInexistant,
            id="recrutement_of_another_organisme",
        ),
    ],
)
def test_raises(scenario, expected_error):
    agent, organisme_id, recrutement_id = scenario()

    with pytest.raises(expected_error):
        list_candidatures(
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
            utilisateur=agent.utilisateur,
        )
