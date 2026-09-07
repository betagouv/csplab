from uuid import uuid4

import pytest

from application.recruteur.services.search_agent_by_email import search_agent_by_email
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


def test_responsable_finds_agent_by_email(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    autre_agent = AgentDjangoFactory()

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(responsable.utilisateur),
        email=autre_agent.utilisateur.email,
    )

    assert result is not None
    assert result.utilisateur_id == autre_agent.utilisateur_id


def test_responsable_gets_none_for_unknown_email(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(responsable.utilisateur),
        email="inconnu@example.com",
    )

    assert result is None


def test_membre_is_denied(db):
    membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
    autre_agent = AgentDjangoFactory()

    with pytest.raises(AccesOrganismeRefuse):
        search_agent_by_email(
            organisme_id=organisme.id,
            utilisateur=UtilisateurMapper().to_domain(membre.utilisateur),
            email=autre_agent.utilisateur.email,
        )


def test_staff_without_role_is_authorized(db):
    _, organisme = create_organisme_with_agent()
    autre_agent = AgentDjangoFactory()
    staff = UtilisateurDjangoFactory(is_staff=True)

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(staff),
        email=autre_agent.utilisateur.email,
    )

    assert result is not None
    assert result.utilisateur_id == autre_agent.utilisateur_id


def test_unknown_organisme_raises(db):
    utilisateur = UtilisateurMapper().to_domain(UtilisateurDjangoFactory())

    with pytest.raises(OrganismeNexistePas):
        search_agent_by_email(
            organisme_id=uuid4(),
            utilisateur=utilisateur,
            email="inconnu@example.com",
        )
