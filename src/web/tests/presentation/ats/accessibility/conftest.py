import pytest
from playwright.sync_api import Page

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel

RECRUTEMENT = "Responsable RH"
CANDIDAT = "Alice"


@pytest.fixture
def superviseure_page(sign_in) -> Page:
    return sign_in("Marie")


@pytest.fixture
def recrutement_url(organisme_url, seeded_recruteur) -> str:
    recrutement = RecrutementModel.objects.get(offre__title=RECRUTEMENT)
    return f"{organisme_url}/recrutements/{recrutement.pk}"


@pytest.fixture
def candidature_url(recrutement_url, seeded_recruteur) -> str:
    candidature = CandidatureModel.objects.get(
        etape__recrutement__offre__title=RECRUTEMENT,
        candidat__utilisateur__first_name=CANDIDAT,
    )
    return f"{recrutement_url}/candidatures/{candidature.pk}"
