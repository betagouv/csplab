from uuid import uuid4

from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_organisme,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

ACTIONS_DU_RESPONSABLE = {"search_agent", "create_agent"}


def _actions_of_agent(organisme_ids_responsable, organisme_id):
    return set(
        authorized_actions_of_organisme(
            AgentOrganismeRole.AGENT,
            organisme_id,
            utilisateur=UtilisateurDjangoFactory.build(),
            organisme_ids_responsable=organisme_ids_responsable,
        )
    )


def test_agent_responsable_of_a_recrutement_gets_the_responsable_actions():
    organisme_id = uuid4()

    actions = _actions_of_agent({organisme_id}, organisme_id)

    assert ACTIONS_DU_RESPONSABLE <= actions


def test_agent_not_responsable_does_not_get_the_responsable_actions():
    actions = _actions_of_agent(frozenset(), uuid4())

    assert not ACTIONS_DU_RESPONSABLE & actions
