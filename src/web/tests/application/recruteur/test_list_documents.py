from application.recruteur.services.list_documents import list_documents
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)


def test_authorized_agent_lists_the_documents(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)
    autre_candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    DocumentDjangoFactory(candidature=autre_candidature)

    result = list_documents(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        utilisateur=agent.utilisateur,
    )

    assert list(result) == [document]
