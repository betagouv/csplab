from uuid import uuid4

import pytest

from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_etapes,
    authorized_actions_of_organisme,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement as Categorie,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)

ACTIONS_DU_RESPONSABLE = {"search_agent", "create_agent"}
ACTION = OrganismeAction.UPDATE_ORGANISME_STEPS


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


@pytest.fixture
def organisme(db):
    return OrganismeDjangoFactory()


@pytest.fixture
def staff():
    return UtilisateurDjangoFactory(is_staff=True)


@pytest.mark.parametrize("nb_en_cours", [1, 3])
def test_without_the_right_to_modify_no_etape_has_actions(organisme, nb_en_cours):
    categories = [
        Categorie.ENTREE,
        *[Categorie.EN_COURS] * nb_en_cours,
        Categorie.REFUS,
        Categorie.ACCEPTE,
    ]

    assert authorized_actions_of_etapes(
        categories,
        action=ACTION,
        organisme_id=organisme.id,
        utilisateur=UtilisateurDjangoFactory(),
    ) == [[] for _ in categories]


def test_an_etape_with_candidatures_cannot_be_deleted(organisme, staff):
    categories = [Categorie.ENTREE, Categorie.EN_COURS, Categorie.EN_COURS]

    actions = authorized_actions_of_etapes(
        categories,
        action=ACTION,
        organisme_id=organisme.id,
        utilisateur=staff,
        nb_candidatures=[0, 3, 0],
    )

    assert "delete_etape" not in actions[1]
    assert "delete_etape" in actions[2]


@pytest.mark.parametrize(
    "recrutement_role",
    [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR],
)
def test_agent_with_a_lower_recrutement_role_has_no_etape_actions(db, recrutement_role):
    utilisateur = UtilisateurDjangoFactory()
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=utilisateur
    )
    recrutement = RecrutementDjangoFactory(
        organisme=organisme,
        etapes=[],
        agent_link__agent=agent,
        agent_link__role=recrutement_role.value,
    )

    actions = authorized_actions_of_etapes(
        [Categorie.ENTREE, Categorie.EN_COURS],
        action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        utilisateur=utilisateur,
    )

    assert actions == [[], []]
