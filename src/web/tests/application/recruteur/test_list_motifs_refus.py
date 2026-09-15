from uuid import uuid4

import pytest

from application.recruteur.services.list_motifs_refus import list_motifs_refus
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


@pytest.mark.parametrize(
    "role", [AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT]
)
def test_agent_gets_full_motifs_list(db, role):
    agent, organisme = create_organisme_with_agent(role=role)

    result = list_motifs_refus(
        organisme_id=organisme.id,
        utilisateur=UtilisateurMapper().to_domain(agent.utilisateur),
    )

    assert result == list(MotifRefus)


def test_staff_without_role_is_denied(db):
    _, organisme = create_organisme_with_agent()
    staff = UtilisateurDjangoFactory(is_staff=True)

    with pytest.raises(AccesOrganismeRefuse):
        list_motifs_refus(
            organisme_id=organisme.id,
            utilisateur=UtilisateurMapper().to_domain(staff),
        )


def test_non_agent_is_denied(db):
    _, organisme = create_organisme_with_agent()
    autre_utilisateur = UtilisateurDjangoFactory()

    with pytest.raises(AccesOrganismeRefuse):
        list_motifs_refus(
            organisme_id=organisme.id,
            utilisateur=UtilisateurMapper().to_domain(autre_utilisateur),
        )


def test_unknown_organisme_raises(db):
    utilisateur = UtilisateurMapper().to_domain(UtilisateurDjangoFactory())

    with pytest.raises(OrganismeNexistePas):
        list_motifs_refus(
            organisme_id=uuid4(),
            utilisateur=utilisateur,
        )
