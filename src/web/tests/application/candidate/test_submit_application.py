from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
import time_machine

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from application.candidate.usecases.submit_application import SubmitApplicationUsecase
from domain.candidate.events.candidature_events import (
    CandidatureSoumise,
    DossierCandidatureInitialise,
)
from domain.candidate.exceptions.candidature_errors import CandidatureDejaSoumise
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory

_FROZEN_TS = datetime.now(tz=timezone.utc)


@pytest.fixture
def submit_application_usecase():
    recrutement_repository = MagicMock(spec=IRecrutementRepository)
    candidat_repository = MagicMock(spec=ICandidatRepository)
    candidature_repository = MagicMock(spec=ICandidatureRepository)
    candidature_repository.exists_by_candidat_and_offre.return_value = False
    return SubmitApplicationUsecase(
        recrutement_repository=recrutement_repository,
        candidat_repository=candidat_repository,
        candidature_repository=candidature_repository,
        audit_log_writer=MagicMock(spec=AuditLogWriter),
        logger=MagicMock(),
    )


@time_machine.travel(_FROZEN_TS, tick=False)
def test_submit_application_success(submit_application_usecase):
    offre_id = uuid4()
    candidat = CandidatFactory.create_entity()

    recrutement = RecrutementFactory.create_entity(
        offre_id=offre_id, derniere_activite_le=_FROZEN_TS
    )

    submit_application_usecase.candidat_repository.get_by_id.return_value = candidat
    submit_application_usecase.recrutement_repository.get_by_id.return_value = (
        recrutement
    )

    candidature = submit_application_usecase.execute(
        command=SubmitApplicationCommand(
            offre_id=offre_id, candidat_id=candidat.entity_id
        )
    )

    events = candidature.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[0], DossierCandidatureInitialise)
    assert isinstance(events[1], CandidatureSoumise)
    assert candidature.statut == StatutCandidature.SOUMISE
    submit_application_usecase.candidature_repository.save.assert_called_once()

    assert submit_application_usecase.audit_log_writer.drain_events.call_count == 1


def test_submit_application_raises_when_candidat_not_found(submit_application_usecase):
    candidat_id = uuid4()
    submit_application_usecase.candidat_repository.get_by_id.side_effect = (
        CandidatInexistant(candidat_id)
    )

    with pytest.raises(CandidatInexistant):
        submit_application_usecase.execute(
            command=SubmitApplicationCommand(offre_id=uuid4(), candidat_id=candidat_id)
        )


def test_submit_application_raises_when_recrutement_not_found(
    submit_application_usecase,
):
    offre_id = uuid4()
    submit_application_usecase.recrutement_repository.get_by_id.side_effect = (
        RecrutementInexistant(offre_id)
    )

    with pytest.raises(RecrutementInexistant):
        submit_application_usecase.execute(
            command=SubmitApplicationCommand(offre_id=offre_id, candidat_id=uuid4())
        )


def test_submit_candidature_twice(submit_application_usecase):
    offre_id = uuid4()
    candidat_id = uuid4()

    submit_application_usecase.candidat_repository.get_by_id.return_value = MagicMock()
    submit_application_usecase.recrutement_repository.get_by_id.return_value = (
        MagicMock()
    )
    submit_application_usecase.candidature_repository.exists_by_candidat_and_offre.return_value = (  # noqa: E501
        True
    )

    with pytest.raises(CandidatureDejaSoumise):
        submit_application_usecase.execute(
            command=SubmitApplicationCommand(offre_id=offre_id, candidat_id=candidat_id)
        )
