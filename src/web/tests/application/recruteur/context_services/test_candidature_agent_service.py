from uuid import uuid4

import pytest

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.services.conversation_stubs import stub_conversation_id
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)

OBJET = "Convocation à l'entretien"


class TestCheckCandidatureBelongsToRecrutement:
    def test_passes_when_candidature_belongs_to_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )

        CandidatureAgentService(
            recrutement_id=recrutement.pk, candidature_id=candidature.pk
        ).check_candidature_belongs_to_recrutement()

    def test_raises_when_candidature_from_another_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        other_candidature = CandidatureDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            CandidatureAgentService(
                recrutement_id=recrutement.pk, candidature_id=other_candidature.pk
            ).check_candidature_belongs_to_recrutement()

    def test_raises_when_candidature_does_not_exist(self, db):
        recrutement = RecrutementDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            CandidatureAgentService(
                recrutement_id=recrutement.pk, candidature_id=uuid4()
            ).check_candidature_belongs_to_recrutement()


class TestCheckConversationBelongsToCandidature:
    def test_passes_when_conversation_belongs_to_candidature(self):
        candidature_id = uuid4()

        CandidatureAgentService(
            recrutement_id=uuid4(), candidature_id=candidature_id
        ).check_conversation_belongs_to_candidature(
            stub_conversation_id(candidature_id, OBJET)
        )

    def test_raises_when_conversation_belongs_to_another_candidature(self):
        with pytest.raises(ConversationInexistante):
            CandidatureAgentService(
                recrutement_id=uuid4(), candidature_id=uuid4()
            ).check_conversation_belongs_to_candidature(
                stub_conversation_id(uuid4(), OBJET)
            )

    def test_raises_when_conversation_does_not_exist(self):
        with pytest.raises(ConversationInexistante):
            CandidatureAgentService(
                recrutement_id=uuid4(), candidature_id=uuid4()
            ).check_conversation_belongs_to_candidature(uuid4())
