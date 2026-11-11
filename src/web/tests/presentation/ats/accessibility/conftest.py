import pytest
from playwright.sync_api import Page

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from tests.presentation.ats.seed import CANDIDAT_FIRST_NAME


@pytest.fixture
def superviseur_page(sign_in) -> Page:
    return sign_in("Marie")


@pytest.fixture
def candidature_url(recrutement_url, recrutement) -> str:
    candidature = CandidatureModel.objects.get(
        etape__recrutement=recrutement,
        candidat__utilisateur__first_name=CANDIDAT_FIRST_NAME,
    )
    return f"{recrutement_url}/candidatures/{candidature.pk}"
