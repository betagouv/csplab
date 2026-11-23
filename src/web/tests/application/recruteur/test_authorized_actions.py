from uuid import uuid4

import pytest

from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_etapes,
    authorized_actions_of_organisme,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement as Categorie,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
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


@pytest.fixture
def organisme(db):
    return OrganismeDjangoFactory()


@pytest.fixture
def staff():
    return UtilisateurDjangoFactory(is_staff=True)


def test_the_only_en_cours_etape_cannot_be_deleted(organisme, staff):
    categories = [
        Categorie.ENTREE,
        Categorie.EN_COURS,
        Categorie.REFUS,
        Categorie.ACCEPTE,
    ]

    actions = authorized_actions_of_etapes(
        categories, organisme_id=organisme.id, utilisateur=staff
    )

    assert actions[1] == [
        "edit_etape",
        "insert_etape_before",
        "insert_etape_after",
    ]


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
        organisme_id=organisme.id,
        utilisateur=UtilisateurDjangoFactory(),
    ) == [[] for _ in categories]
