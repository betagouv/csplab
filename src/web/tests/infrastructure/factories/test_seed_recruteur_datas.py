import secrets

import filetype
from django.contrib.auth import authenticate

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.factories.seed_recruteur_datas import (
    _ADMIN_SPEC,
    _AGENTS_SPECS,
    _CANDIDATS_SPECS,
    seed_recruteur_datas,
)

SEED_EMAILS = [
    _AGENTS_SPECS[0]["email"],
    _ADMIN_SPEC["email"],
    _CANDIDATS_SPECS[0]["email"],
]


class TestSeedRecruteurDatas:
    def test_accounts_log_in_with_the_configured_password(self, db, monkeypatch):
        password = secrets.token_urlsafe()
        monkeypatch.setenv("SEED_USER_PASSWORD", password)

        seed_recruteur_datas()

        for email in SEED_EMAILS:
            assert authenticate(username=email, password=password) is not None, email

    def test_accounts_log_in_with_the_generated_password(self, db, monkeypatch):
        monkeypatch.delenv("SEED_USER_PASSWORD", raising=False)

        context = seed_recruteur_datas()

        user = authenticate(
            username=_AGENTS_SPECS[0]["email"], password=context["seed_password"]
        )
        assert user is not None

    def test_submitted_candidatures_carry_a_pdf_cv_and_survive_a_reseed(self, db):
        seed_recruteur_datas()
        seed_recruteur_datas(force=True)

        soumises = CandidatureModel.objects.filter(
            statut=StatutCandidature.SOUMISE.value
        )
        cvs = DocumentModel.objects.filter(type_document=TypeDocument.CV.value)
        assert set(cvs.values_list("candidature_id", flat=True)) == set(
            soumises.values_list("id", flat=True)
        )
        with cvs.first().fichier.open("rb") as fichier:  # type: ignore[union-attr]
            assert filetype.guess(fichier.read(262)).mime == "application/pdf"
