from uuid import uuid4

import pytest

from application.recruteur.services.get_organisme_etapes import get_organisme_etapes
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


def test_superviseur_gets_organisme(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    result = get_organisme_etapes(
        organisme_id=organisme.id, utilisateur=agent.utilisateur
    )

    assert result.id == organisme.id


def test_staff_without_liaison_gets_organisme(db):
    organisme = OrganismeDjangoFactory()
    staff = UtilisateurDjangoFactory(is_staff=True)

    result = get_organisme_etapes(organisme_id=organisme.id, utilisateur=staff)

    assert result.id == organisme.id


def test_membre_is_denied(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

    with pytest.raises(AccesOrganismeRefuse):
        get_organisme_etapes(organisme_id=organisme.id, utilisateur=agent.utilisateur)


def test_superviseur_of_another_organisme_is_denied(db):
    organisme = OrganismeDjangoFactory()
    autre_superviseur, _ = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )

    with pytest.raises(AccesOrganismeRefuse):
        get_organisme_etapes(
            organisme_id=organisme.id, utilisateur=autre_superviseur.utilisateur
        )


def test_unknown_organisme_raises(db):
    with pytest.raises(OrganismeNexistePas):
        get_organisme_etapes(
            organisme_id=uuid4(), utilisateur=UtilisateurDjangoFactory()
        )
