from uuid import uuid4

import pytest
from django.utils import timezone

from application.recruteur.services.get_recrutement_detail import (
    get_recrutement_detail,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.etape import etapes_ordonnees
from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _utilisateur(agent) -> UserModel:
    return agent.utilisateur


def _agent_without_role_in_organisme():
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent, organisme.id, recrutement.pk


def _agent_revoked_from_organisme():
    organisme = OrganismeDjangoFactory()
    agent = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.SUPERVISEUR.value,
        date_revocation=timezone.now(),
    ).agent
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    return agent, organisme.id, recrutement.pk


def _agent_with_revoked_recrutement_role():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=agent,
        role=AgentRecrutementRole.RESPONSABLE.value,
        date_revocation=timezone.now(),
    )
    return agent, organisme.id, recrutement.pk


def _agent_on_unknown_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    return agent, organisme.id, uuid4()


def _superviseur_on_unknown_organisme():
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent, uuid4(), uuid4()


def _superviseur_on_deleted_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    organisme.supprime_le = timezone.now()
    organisme.save(update_fields=["supprime_le"])
    return agent, organisme.id, recrutement.pk


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
            _agent_revoked_from_organisme,
            AccesOrganismeRefuse,
            id="revoked_from_organisme",
        ),
        pytest.param(
            _agent_with_revoked_recrutement_role,
            AccesRecrutementRefuse,
            id="revoked_recrutement_role",
        ),
        pytest.param(
            _agent_on_unknown_recrutement,
            AccesRecrutementRefuse,
            id="permission_checked_before_existence",
        ),
        pytest.param(
            _superviseur_on_unknown_organisme,
            OrganismeNexistePas,
            id="unknown_organisme",
        ),
        pytest.param(
            _superviseur_on_deleted_organisme,
            OrganismeNexistePas,
            id="deleted_organisme",
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
        get_recrutement_detail(
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
            utilisateur=_utilisateur(agent),
        )


def test_offre_with_nullable_columns_is_returned():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    offre = OfferDjangoFactory(
        area=None,
        country=None,
        region=None,
        department=None,
        location_label=None,
        latitude=None,
        longitude=None,
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offre)

    result = get_recrutement_detail(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        utilisateur=_utilisateur(agent),
    )

    assert result.offre.country is None
    assert result.offre.latitude is None


def test_etapes_ordonnees_ignores_stale_and_missing_ids():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    etapes = list(recrutement.etapes.all())
    recrutement.ordre_etapes = [str(uuid4()), str(etapes[0].id)]
    recrutement.save(update_fields=["ordre_etapes"])

    result = get_recrutement_detail(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        utilisateur=_utilisateur(agent),
    )

    assert etapes_ordonnees(result) == [etapes[0]]
