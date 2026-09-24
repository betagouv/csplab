from uuid import uuid4

import pytest

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.services.conversation_stubs import (
    _CONVERSATIONS,
    stub_conversation_id,
)
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

OBJET = _CONVERSATIONS[0][0]


def _service(candidature_id, recrutement_id=None):
    return CandidatureAgentService(
        recrutement_id=recrutement_id or uuid4(), candidature_id=candidature_id
    )


class TestCheckCandidatureBelongsToRecrutement:
    def test_passes_when_candidature_belongs_to_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        candidature = CandidatureDjangoFactory(
            etape=EtapeDjangoFactory(recrutement=recrutement)
        )

        _service(
            candidature.pk, recrutement.pk
        ).check_candidature_belongs_to_recrutement()

    def test_raises_when_candidature_from_another_recrutement(self, db):
        recrutement = RecrutementDjangoFactory()
        other_candidature = CandidatureDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            _service(
                other_candidature.pk, recrutement.pk
            ).check_candidature_belongs_to_recrutement()

    def test_raises_when_candidature_does_not_exist(self, db):
        recrutement = RecrutementDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            _service(uuid4(), recrutement.pk).check_candidature_belongs_to_recrutement()


class TestCheckConversationBelongsToCandidature:
    def test_passes_when_conversation_belongs_to_candidature(self):
        candidature_id = uuid4()

        _service(candidature_id).check_conversation_belongs_to_candidature(
            stub_conversation_id(candidature_id, OBJET)
        )

    def test_raises_when_conversation_belongs_to_another_candidature(self):
        with pytest.raises(ConversationInexistante):
            _service(uuid4()).check_conversation_belongs_to_candidature(
                stub_conversation_id(uuid4(), OBJET)
            )

    def test_raises_when_conversation_does_not_exist(self):
        with pytest.raises(ConversationInexistante):
            _service(uuid4()).check_conversation_belongs_to_candidature(uuid4())
