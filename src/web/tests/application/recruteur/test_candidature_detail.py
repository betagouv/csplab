from datetime import timedelta
from uuid import uuid4

import pytest
from django.utils import timezone

from application.recruteur.services.candidature_detail import get_candidature_detail
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)


def _utilisateur(entity_id):
    return UtilisateurFactory.create_entity(entity_id=entity_id)


def _get_detail(agent, organisme, recrutement, candidature):
    return get_candidature_detail(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )


def test_returns_candidature_with_ordered_etapes(db):
    agent, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent()
    etape = recrutement.etapes.get(id=recrutement.ordre_etapes[1])
    candidature = CandidatureDjangoFactory(etape=etape)

    result = _get_detail(agent, organisme, recrutement, candidature)

    assert result.candidature == candidature
    assert result.candidature.etape == etape
    assert [str(e.id) for e in result.etapes] == recrutement.ordre_etapes


def test_document_is_the_latest_cv(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    older_cv = DocumentDjangoFactory(
        candidature=candidature, type_document=TypeDocument.CV
    )
    latest_cv = DocumentDjangoFactory(
        candidature=candidature, type_document=TypeDocument.CV
    )
    DocumentModel.objects.filter(pk=older_cv.pk).update(
        created_at=timezone.now() - timedelta(days=1)
    )
    DocumentDjangoFactory(
        candidature=candidature, type_document=TypeDocument.LETTRE_MOTIVATION
    )

    result = _get_detail(agent, organisme, recrutement, candidature)

    assert result.document_uuid == latest_cv.id


def test_document_is_none_without_cv(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    DocumentDjangoFactory(
        candidature=candidature, type_document=TypeDocument.LETTRE_MOTIVATION
    )

    result = _get_detail(agent, organisme, recrutement, candidature)

    assert result.document_uuid is None


def test_navigation_lists_candidatures_of_the_same_etape_in_creation_order(db):
    agent, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent()
    etape = EtapeDjangoFactory(recrutement=recrutement)
    derniere = CandidatureDjangoFactory(etape=etape)
    candidature = CandidatureDjangoFactory(etape=etape)
    premiere = CandidatureDjangoFactory(etape=etape)
    now = timezone.now()
    for days_ago, c in ((3, premiere), (2, candidature), (1, derniere)):
        CandidatureModel.objects.filter(pk=c.pk).update(
            created_at=now - timedelta(days=days_ago)
        )
    CandidatureDjangoFactory(etape=EtapeDjangoFactory(recrutement=recrutement))

    result = _get_detail(agent, organisme, recrutement, candidature)

    assert result.navigation_candidature_uuids == [
        premiere.id,
        candidature.id,
        derniere.id,
    ]


def test_agent_member_of_recrutement_gets_the_detail(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=agent,
        role=AgentRecrutementRole.CONTRIBUTEUR.value,
    )
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)

    result = _get_detail(agent, organisme, recrutement, candidature)

    assert result.candidature == candidature


def _kwargs(utilisateur_id, organisme, recrutement, candidature):
    return {
        "organisme_id": organisme.id,
        "recrutement_id": recrutement.pk,
        "candidature_id": candidature.pk,
        "utilisateur": _utilisateur(utilisateur_id),
    }


def _agent_not_member_of_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return _kwargs(agent.utilisateur_id, organisme, recrutement, candidature)


def _user_without_organisme_role():
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return _kwargs(uuid4(), organisme, recrutement, candidature)


def _unknown_organisme():
    return {
        "organisme_id": uuid4(),
        "recrutement_id": uuid4(),
        "candidature_id": uuid4(),
        "utilisateur": _utilisateur(uuid4()),
    }


def _recrutement_not_under_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement = RecrutementDjangoFactory(organisme=OrganismeDjangoFactory())
    candidature = CandidatureDjangoFactory(etape__recrutement=other_recrutement)
    return _kwargs(agent.utilisateur_id, organisme, other_recrutement, candidature)


def _candidature_of_another_recrutement():
    agent, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent()
    other_candidature = CandidatureDjangoFactory(
        etape__recrutement=RecrutementDjangoFactory(organisme=organisme)
    )
    return _kwargs(agent.utilisateur_id, organisme, recrutement, other_candidature)


@pytest.mark.parametrize(
    ("build_kwargs", "expected_error"),
    [
        pytest.param(
            _agent_not_member_of_recrutement,
            AccesRecrutementRefuse,
            id="agent_not_member_of_recrutement",
        ),
        pytest.param(
            _user_without_organisme_role,
            AccesOrganismeRefuse,
            id="user_without_organisme_role",
        ),
        pytest.param(
            _unknown_organisme,
            OrganismeNexistePas,
            id="unknown_organisme",
        ),
        pytest.param(
            _recrutement_not_under_organisme,
            RecrutementInexistant,
            id="recrutement_not_under_organisme",
        ),
        pytest.param(
            _candidature_of_another_recrutement,
            RecrutementCandidatureInexistante,
            id="candidature_of_another_recrutement",
        ),
    ],
)
def test_access_is_denied(db, build_kwargs, expected_error):
    with pytest.raises(expected_error):
        get_candidature_detail(**build_kwargs())
