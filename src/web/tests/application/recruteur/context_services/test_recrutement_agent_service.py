from uuid import uuid4

import pytest
from django.utils import timezone

from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.errors.recrutement_agent_errors import (
    AgentDejaMembreRecrutement,
    AgentNonMembreRecrutement,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentInexistant,
    RecrutementInexistant,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)


class TestCheckRecrutementBelongsToOrganisme:
    def test_passes_when_recrutement_belongs_to_organisme(self, db):
        recrutement = RecrutementDjangoFactory()

        RecrutementAgentService(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.pk,
        ).check_recrutement_belongs_to_organisme()

    def test_raises_when_recrutement_belongs_to_another_organisme(self, db):
        recrutement = RecrutementDjangoFactory()
        other_organisme = OrganismeDjangoFactory()

        with pytest.raises(RecrutementInexistant):
            RecrutementAgentService(
                organisme_id=other_organisme.id,
                recrutement_id=recrutement.pk,
            ).check_recrutement_belongs_to_organisme()

    def test_raises_when_recrutement_does_not_exist(self, db):
        organisme = OrganismeDjangoFactory()

        with pytest.raises(RecrutementInexistant):
            RecrutementAgentService(
                organisme_id=organisme.id,
                recrutement_id=uuid4(),
            ).check_recrutement_belongs_to_organisme()


class TestCheckDocumentBelongsToRecrutement:
    def test_passes_when_document_belongs_to_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )
        document = DocumentDjangoFactory(candidature=candidature)

        RecrutementAgentService(
            organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
        ).check_document_belongs_to_recrutement(candidature.pk, document.pk)

    def test_raises_when_document_from_another_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        other_document = DocumentDjangoFactory()

        with pytest.raises(RecrutementDocumentInexistant):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).check_document_belongs_to_recrutement(
                other_document.candidature_id, other_document.pk
            )

    def test_raises_when_document_from_different_candidature(self, db):
        recrutement = RecrutementDjangoFactory()
        etape = EtapeDjangoFactory(recrutement=recrutement)
        candidature = CandidatureDjangoFactory(etape=etape)
        other_candidature = CandidatureDjangoFactory(etape=etape)
        document = DocumentDjangoFactory(candidature=candidature)

        with pytest.raises(RecrutementDocumentInexistant):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).check_document_belongs_to_recrutement(other_candidature.pk, document.pk)

    def test_raises_when_document_does_not_exist(self, db):
        recrutement = RecrutementDjangoFactory()
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )

        with pytest.raises(RecrutementDocumentInexistant):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).check_document_belongs_to_recrutement(candidature.pk, uuid4())


class TestCheckAgentAttachedToOrganisme:
    def test_passes_when_agent_is_an_active_member(self, db):
        organisme = OrganismeDjangoFactory()
        agent = OrganismeAgentDjangoFactory(organisme=organisme).agent

        RecrutementAgentService(
            organisme_id=organisme.id, recrutement_id=uuid4()
        ).check_agent_attached_to_organisme(agent.utilisateur_id)

    def test_raises_when_agent_is_not_attached(self, db):
        organisme = OrganismeDjangoFactory()
        agent = AgentDjangoFactory()

        with pytest.raises(AgentNonRattache):
            RecrutementAgentService(
                organisme_id=organisme.id, recrutement_id=uuid4()
            ).check_agent_attached_to_organisme(agent.utilisateur_id)

    def test_raises_when_agent_membership_is_revoked(self, db):
        organisme = OrganismeDjangoFactory()
        agent = OrganismeAgentDjangoFactory(
            organisme=organisme, date_revocation=timezone.now()
        ).agent

        with pytest.raises(AgentNonRattache):
            RecrutementAgentService(
                organisme_id=organisme.id, recrutement_id=uuid4()
            ).check_agent_attached_to_organisme(agent.utilisateur_id)

    def test_raises_when_agent_attached_to_another_organisme(self, db):
        organisme = OrganismeDjangoFactory()
        agent = OrganismeAgentDjangoFactory().agent

        with pytest.raises(AgentNonRattache):
            RecrutementAgentService(
                organisme_id=organisme.id, recrutement_id=uuid4()
            ).check_agent_attached_to_organisme(agent.utilisateur_id)


class TestCheckAgentNotActiveMember:
    def test_passes_when_agent_has_no_membership(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()

        RecrutementAgentService(
            organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
        ).check_agent_not_active_member(agent.utilisateur_id)

    def test_passes_when_agent_membership_is_revoked(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=agent, date_revocation=timezone.now()
        )

        RecrutementAgentService(
            organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
        ).check_agent_not_active_member(agent.utilisateur_id)

    def test_raises_when_agent_is_already_an_active_member(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()
        RecrutementAgentDjangoFactory(recrutement=recrutement, agent=agent)

        with pytest.raises(AgentDejaMembreRecrutement):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).check_agent_not_active_member(agent.utilisateur_id)


class TestGetActiveMember:
    def test_returns_the_active_member(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()
        membership = RecrutementAgentDjangoFactory(recrutement=recrutement, agent=agent)

        result = RecrutementAgentService(
            organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
        ).get_active_member(agent.utilisateur_id)

        assert result.pk == membership.pk

    def test_raises_when_agent_has_no_membership(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()

        with pytest.raises(AgentNonMembreRecrutement):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).get_active_member(agent.utilisateur_id)

    def test_raises_when_agent_membership_is_revoked(self, db):
        recrutement = RecrutementDjangoFactory()
        agent = AgentDjangoFactory()
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=agent, date_revocation=timezone.now()
        )

        with pytest.raises(AgentNonMembreRecrutement):
            RecrutementAgentService(
                organisme_id=recrutement.organisme_id, recrutement_id=recrutement.pk
            ).get_active_member(agent.utilisateur_id)
