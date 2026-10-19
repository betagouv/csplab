from io import BytesIO, StringIO
from uuid import UUID

import pytest
from django.core.management import CommandError, call_command
from django.db.models import Count, F
from django.utils import timezone
from pypdf import PdfReader

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.messagerie.models import (
    ConversationLectureModel,
    ConversationModel,
    MessageModel,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)

DIJOP_ID = UUID("f38d4d0f-7c17-592a-a371-d9205fca97f6")
DIJOP_SIRET = "93466293300019"

COMPTES_ATTENDUS = {
    "offres": 11,
    "recrutements_en_cours": 8,
    "recrutements_archives": 3,
    "responsables": 11,
    "candidatures": 303,
    "candidats": 303,
    "cvs": 303,
    "par_etape": {
        "Réception des candidatures": 144,
        "Présélection": 51,
        "Entretien": 35,
        "Proposition": 16,
        "Refus": 54,
        "Recrutement": 3,
    },
    "recrutements_finalises": [
        "DEMO-1945-009",
        "DEMO-1945-010",
        "DEMO-1945-011",
    ],
    "notes": 38,
    "conversations": 27,
    "messages": 54,
    "reponses_candidat": 27,
    "lectures": 28,
}


def _dijop(**kwargs):
    return OrganismeDjangoFactory(id=DIJOP_ID, siret=DIJOP_SIRET, nom="DIJOP", **kwargs)


def _dijop_avec_agents():
    dijop = _dijop()
    OrganismeAgentDjangoFactory(
        organisme=dijop, role=AgentOrganismeRole.SUPERVISEUR.value
    )
    OrganismeAgentDjangoFactory(organisme=dijop)
    return dijop


def _seed(*options, stdout=None):
    call_command(
        "seed_demo_organisme",
        "--organisme",
        str(DIJOP_ID),
        *options,
        stdout=stdout or StringIO(),
    )


def _candidatures_demo():
    return CandidatureModel.objects.filter(
        etape__recrutement__offre__reference__startswith="DEMO-1945-"
    )


def _comptes():
    candidatures = _candidatures_demo()
    recrutements = RecrutementModel.objects.filter(
        offre__reference__startswith="DEMO-1945-"
    )
    return {
        "offres": OfferModel.objects.filter(reference__startswith="DEMO-1945-").count(),
        "recrutements_en_cours": recrutements.filter(
            offre__archived_at__isnull=True, organisme_id=DIJOP_ID
        ).count(),
        "recrutements_archives": recrutements.filter(
            offre__archived_at__isnull=False, organisme_id=DIJOP_ID
        ).count(),
        "responsables": RecrutementAgentModel.objects.filter(
            recrutement__in=recrutements,
            role=AgentRecrutementRole.RESPONSABLE.value,
        ).count(),
        "candidatures": candidatures.count(),
        "candidats": UserModel.objects.filter(
            email__endswith="@demo.candidat.fr"
        ).count(),
        "cvs": DocumentModel.objects.filter(
            candidature__in=candidatures, type_document="cv"
        ).count(),
        "par_etape": dict(
            candidatures.values("etape__nom")
            .annotate(n=Count("id"))
            .values_list("etape__nom", "n")
        ),
        "recrutements_finalises": sorted(
            candidatures.filter(etape__nom="Recrutement").values_list(
                "etape__recrutement__offre__reference", flat=True
            )
        ),
        "notes": NoteModel.objects.filter(candidature__in=candidatures).count(),
        "conversations": ConversationModel.objects.filter(
            candidature__in=candidatures, objet="Date d’entretien"
        ).count(),
        "messages": MessageModel.objects.filter(
            conversation__candidature__in=candidatures
        ).count(),
        "reponses_candidat": MessageModel.objects.filter(
            conversation__candidature__in=candidatures,
            auteur_id=F("conversation__candidature__candidat_id"),
        ).count(),
        "lectures": ConversationLectureModel.objects.filter(
            conversation__candidature__in=candidatures
        ).count(),
    }


class TestSeedDemoOrganisme:
    def test_seeds_the_demo_and_force_only_removes_marked_data(self, db):
        dijop = _dijop_avec_agents()
        _, candidature_dijop = create_recrutement_with_candidature(organisme=dijop)
        _, candidature_ailleurs = create_recrutement_with_candidature()

        _seed()

        assert _comptes() == COMPTES_ATTENDUS
        assert (
            not _candidatures_demo()
            .filter(created_at__lt=F("etape__recrutement__offre__publication_date"))
            .exists()
        )
        assert not MessageModel.objects.filter(
            conversation__candidature__in=_candidatures_demo(),
            created_at__lt=F("conversation__candidature__created_at"),
        ).exists()
        simulation = StringIO()
        _seed("--dry-run", stdout=simulation)
        assert (
            "À supprimer avec --force : 11 offres, 303 candidatures, 303 candidats."
            in simulation.getvalue()
        )
        note = NoteModel.objects.filter(candidature__in=_candidatures_demo()).first()
        lignes = note.message.splitlines()  # type: ignore[union-attr]
        assert (lignes[0], len(lignes)) == ("Compte rendu de présélection", 16)
        candidature_005 = (
            _candidatures_demo()
            .filter(etape__recrutement__offre__reference="DEMO-1945-005")
            .first()
        )
        cv = DocumentModel.objects.get(candidature=candidature_005)
        with cv.fichier.open("rb") as fichier:
            texte = "".join(
                page.extract_text() for page in PdfReader(BytesIO(fichier.read())).pages
            )
        nom_complet = candidature_005.candidat.utilisateur.get_full_name()  # type: ignore[union-attr]
        assert nom_complet in texte
        assert "l’État" in texte
        assert nom_complet in candidature_005.candidat.resume  # type: ignore[union-attr]

        sortie = StringIO()
        _seed(stdout=sortie)
        assert "déjà" in sortie.getvalue()
        assert _comptes() == COMPTES_ATTENDUS

        _seed("--force")

        assert _comptes() == COMPTES_ATTENDUS
        assert set(
            CandidatureModel.objects.filter(
                pk__in=[candidature_dijop.pk, candidature_ailleurs.pk]
            ).values_list("pk", flat=True)
        ) == {candidature_dijop.pk, candidature_ailleurs.pk}

    @pytest.mark.parametrize(
        ("cas", "motif"),
        [
            ("organisme_absent", "introuvable ou supprimé"),
            ("organisme_supprime", "introuvable ou supprimé"),
            ("aucun_agent_actif", "aucun agent actif"),
            ("production", "production"),
            ("demo_sur_un_autre_organisme", "autre organisme"),
        ],
    )
    def test_stops_without_writing(self, db, monkeypatch, cas, motif):
        if cas == "organisme_supprime":
            OrganismeAgentDjangoFactory(organisme=_dijop(supprime_le=timezone.now()))
        elif cas == "aucun_agent_actif":
            OrganismeAgentDjangoFactory(
                organisme=_dijop(), date_revocation=timezone.now()
            )
        elif cas == "production":
            _dijop_avec_agents()
            monkeypatch.setenv("SCALEWAY_ENV", "prod")
        elif cas == "demo_sur_un_autre_organisme":
            _dijop_avec_agents()
            RecrutementDjangoFactory(offre__reference="DEMO-1945-001")

        with pytest.raises(CommandError, match=motif):
            _seed("--force")

        offres = OfferModel.objects.filter(reference__startswith="DEMO-1945-")
        if cas == "demo_sur_un_autre_organisme":
            assert list(offres.values_list("reference", flat=True)) == ["DEMO-1945-001"]
            assert (
                RecrutementModel.objects.exclude(organisme_id=DIJOP_ID)
                .filter(offre__reference="DEMO-1945-001")
                .exists()
            )
        else:
            assert not offres.exists()
        assert not UserModel.objects.filter(
            email__endswith="@demo.candidat.fr"
        ).exists()

    def test_dry_run_prints_counts_without_writing(self, db):
        _dijop_avec_agents()
        sortie = StringIO()

        _seed("--dry-run", stdout=sortie)

        assert "303" in sortie.getvalue()
        assert not OfferModel.objects.filter(
            reference__startswith="DEMO-1945-"
        ).exists()
        assert not UserModel.objects.filter(
            email__endswith="@demo.candidat.fr"
        ).exists()
