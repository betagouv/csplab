import pytest
from django.utils import timezone

from application.recruteur.services.list_recrutement_agents import (
    list_recrutement_agents,
)
from domain.identite.errors.organisme_permission_errors import AccesRecrutementRefuse
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)


def test_by_recrutement_excludes_revoked_agents(db):
    # RecrutementDjangoFactory auto-creates one active RecrutementAgentModel via its
    # `agent_link` RelatedFactory.
    recrutement = RecrutementDjangoFactory()
    active_id = RecrutementAgentModel.objects.get(recrutement=recrutement).id
    revoked = RecrutementAgentDjangoFactory(
        recrutement=recrutement, date_revocation=timezone.now()
    )

    agent_ids = set(
        RecrutementAgentModel.objects.by_recrutement(recrutement.pk).values_list(
            "id", flat=True
        )
    )

    assert agent_ids == {active_id}
    assert revoked.id not in agent_ids


def test_agent_responsable_of_recrutement_lists_team(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=agent,
        role=AgentRecrutementRole.RESPONSABLE.value,
    )

    result = list_recrutement_agents(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        utilisateur=UtilisateurFactory.create_entity(entity_id=agent.utilisateur_id),
    )

    assert agent.utilisateur_id in {liaison.agent_id for liaison in result}


def test_agent_with_revoked_responsable_role_cannot_list_team(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=agent,
        role=AgentRecrutementRole.RESPONSABLE.value,
        date_revocation=timezone.now(),
    )

    with pytest.raises(AccesRecrutementRefuse):
        list_recrutement_agents(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent.utilisateur_id
            ),
        )


@pytest.mark.parametrize(
    "role", [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR]
)
def test_agent_not_responsable_cannot_list_team(db, role):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(recrutement=recrutement, agent=agent, role=role.value)

    with pytest.raises(AccesRecrutementRefuse):
        list_recrutement_agents(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent.utilisateur_id
            ),
        )
