import pytest

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)

AUTHORIZED_ROLES = pytest.mark.parametrize(
    "organisme_role,recrutement_role",
    [
        (AgentOrganismeRole.SUPERVISEUR, None),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR),
    ],
    ids=["superviseur", "agent_responsable", "agent_recruteur", "agent_contributeur"],
)
HTTP_METHODS = pytest.mark.parametrize("method", ["get", "post"])


def grant(test_user, organisme_role, recrutement_role):
    agent, organisme = create_organisme_with_agent(
        role=organisme_role, utilisateur=test_user
    )
    recrutement, candidature = create_recrutement_with_candidature(organisme)
    if recrutement_role is not None:
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=test_user.profil_agent,
            role=recrutement_role.value,
        )
    return agent, organisme, recrutement, candidature
