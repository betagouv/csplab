from uuid import uuid4

import pytest
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from domain.candidate.events.candidature_events import (
    CandidatureSoumise,
    DossierCandidatureInitialise,
)
from domain.candidate.exceptions.candidature_errors import (
    CandidatureDejaSoumise,
    CandidatureNexistePas,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from tests.factories.candidate.candidature_factory import CandidatureFactory


def test_submit_application_success(submit_application_usecase):
    factory = CandidatureFactory.build()
    submit_application_usecase.candidature_repository.get_by_offer.side_effect = (
        CandidatureNexistePas(factory.candidat_id, factory.offre_id)
    )

    candidature = submit_application_usecase.execute(
        command=SubmitApplicationCommand(
            offre_id=factory.offre_id, candidat_id=factory.candidat_id
        )
    )

    events = candidature.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[0], DossierCandidatureInitialise)
    assert isinstance(events[1], CandidatureSoumise)
    assert candidature.statut == StatutCandidature.SOUMISE


def test_submit_application_failure(submit_application_usecase):
    existing = CandidatureFactory.build(statut=StatutCandidature.SOUMISE)
    submit_application_usecase.candidature_repository.get_by_offer.return_value = (
        existing
    )

    with pytest.raises(CandidatureDejaSoumise):
        candidature = submit_application_usecase.execute(
            command=SubmitApplicationCommand(
                offre_id=existing.offre_id, candidat_id=existing.candidat_id
            )
        )
        events = candidature.collect_events()
        assert len(events) == 0


def test_submit_application_raises_when_candidat_not_found(submit_application_usecase):
    candidat_id = uuid4()
    submit_application_usecase.actors_validator.validate.side_effect = (
        CandidatInexistant(candidat_id)
    )

    with pytest.raises(CandidatInexistant):
        submit_application_usecase.execute(
            command=SubmitApplicationCommand(offre_id=uuid4(), candidat_id=candidat_id)
        )


def test_submit_application_raises_when_offer_not_found(submit_application_usecase):
    offre_id = uuid4()
    submit_application_usecase.actors_validator.validate.side_effect = (
        OfferDoesNotExist(offre_id)
    )

    with pytest.raises(OfferDoesNotExist):
        submit_application_usecase.execute(
            command=SubmitApplicationCommand(offre_id=offre_id, candidat_id=uuid4())
        )
