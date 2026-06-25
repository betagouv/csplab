from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from django.contrib import admin
from django.test import RequestFactory
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.candidate.admin import CandidatureAdmin
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from tests.factories.candidate.candidature_factory import CandidatureFactory


@pytest.fixture
def candidature_admin():
    return CandidatureAdmin(CandidatureModel, admin.site)


@pytest.fixture
def request_():
    return RequestFactory().get("/")


def _unsaved_candidature():
    obj = CandidatureModel(offre_id=uuid4(), candidat_id=str(uuid4()))
    obj.save = Mock()  # guard: must never reach persistence
    return obj


@patch("infrastructure.django_apps.candidate.admin.create_candidate_container")
def test_create_routes_through_usecase(create_container, candidature_admin, request_):
    obj = _unsaved_candidature()
    persisted = CandidatureFactory.build()
    usecase = Mock()
    usecase.execute.return_value = persisted
    create_container().submit_application_usecase.return_value = usecase

    candidature_admin.save_model(request_, obj, form=None, change=False)

    command = usecase.execute.call_args.args[0]
    assert command.offre_id == obj.offre_id
    assert command.candidat_id == obj.candidat_id
    assert obj.id == persisted.entity_id
    assert obj.statut == StatutCandidature.INITIAL.value
    obj.save.assert_not_called()


@patch("infrastructure.django_apps.candidate.admin.create_candidate_container")
def test_create_propagates_domain_invariant_error(
    create_container, candidature_admin, request_
):
    obj = _unsaved_candidature()
    usecase = Mock()
    usecase.execute.side_effect = OfferDoesNotExist(obj.offre_id)
    create_container().submit_application_usecase.return_value = usecase

    with pytest.raises(OfferDoesNotExist):
        candidature_admin.save_model(request_, obj, form=None, change=False)

    obj.save.assert_not_called()
