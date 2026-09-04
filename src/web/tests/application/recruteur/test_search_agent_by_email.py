from uuid import uuid4

import pytest

from application.recruteur.services.search_agent_by_email import search_agent_by_email
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


def test_responsable_finds_agent_by_email(db):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    autre_agent = AgentFactory.create_model()

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(responsable.utilisateur),
        email=autre_agent.utilisateur.email,
    )

    assert result is not None
    assert result.utilisateur_id == autre_agent.utilisateur_id


def test_responsable_gets_none_for_unknown_email(db):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(responsable.utilisateur),
        email="inconnu@example.com",
    )

    assert result is None


def test_membre_is_denied(db):
    membre, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )
    autre_agent = AgentFactory.create_model()

    with pytest.raises(AccesOrganismeRefuse):
        search_agent_by_email(
            organisme_id=organisme.id,
            utilisateur=UtilisateurMapper().to_domain(membre.utilisateur),
            email=autre_agent.utilisateur.email,
        )


def test_staff_without_role_is_authorized(db):
    _, organisme = OrganismeFactory.create_model_with_agent()
    autre_agent = AgentFactory.create_model()
    staff = UtilisateurFactory.create_model(is_staff=True)

    result = search_agent_by_email(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(staff),
        email=autre_agent.utilisateur.email,
    )

    assert result is not None
    assert result.utilisateur_id == autre_agent.utilisateur_id


def test_unknown_organisme_raises(db):
    utilisateur = UtilisateurMapper().to_domain(UtilisateurFactory.create_model())

    with pytest.raises(OrganismeNexistePas):
        search_agent_by_email(
            organisme_id=uuid4(),
            utilisateur=utilisateur,
            email="inconnu@example.com",
        )
