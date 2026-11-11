import pytest
from playwright.sync_api import Page

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel

CANDIDAT = "Alice"


@pytest.fixture
def superviseure_page(sign_in) -> Page:
    return sign_in("Marie")


@pytest.fixture
def candidature_url(recrutement_url, recrutement) -> str:
    candidature = CandidatureModel.objects.get(
        etape__recrutement=recrutement,
        candidat__utilisateur__first_name=CANDIDAT,
    )
    return f"{recrutement_url}/candidatures/{candidature.pk}"
