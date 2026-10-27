import random
from io import BytesIO, StringIO
from uuid import UUID, uuid4

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
from infrastructure.django_apps.ingestion.models.source import SourceModel
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
from infrastructure.factories.seed_demo_cv_corpus import CORPUS
from infrastructure.factories.seed_demo_organisme import (
    _CandidaturePlan,
    _cv,
    _pdf_texte,
    seed_demo_organisme,
)
from infrastructure.factories.seed_demo_specs import RecrutementSpec, SpecOrganisme

# miroir de _SOURCE_DEMO_UUID au 27/10
SOURCE_DEMO_ID = UUID("00000000-0000-0000-0000-000000001945")

# miroir de SPECS_DEMO au 27/10
CLES_DEMO = [
    "transition-ecologique",
    "culture",
    "centre-pompidou",
    "premier-ministre",
    "cour-des-comptes",
    "travail-solidarites",
    "dgafp",
    "economie-finances",
]

_RECRUTEMENTS_REDUITS: list[RecrutementSpec] = [
    {
        "intitule": "Conseiller(ère) finances et garanties de l’État",
        "famille": "finances",
        "archive_depuis_jours": None,
        "repartition": (2, 1, 1, 0, 1, 0),
    },
    {
        "intitule": "Chargé(e) de mission biodiversité",
        "famille": "environnement",
        "archive_depuis_jours": 20,
        "repartition": (0, 0, 0, 0, 3, 1),
    },
    {
        "intitule": "Acheteur(se) public(que)",
        "famille": "achats",
        "archive_depuis_jours": 45,
        "repartition": (1, 1, 1, 0, 1, 0),
    },
]
SPEC_A = SpecOrganisme(cle="a", graine=1, recrutements=_RECRUTEMENTS_REDUITS)
SPEC_B = SpecOrganisme(cle="b", graine=2, recrutements=_RECRUTEMENTS_REDUITS)


def _comptes_reduits(reference_finalisee):
    return {
        "offres": 3,
        "recrutements_en_cours": 1,
        "recrutements_archives": 2,
        "responsables": 3,
        "candidatures": 13,
        "candidats": 13,
        "cvs": 13,
        "par_etape": {
            "Réception des candidatures": 3,
            "Présélection": 2,
            "Entretien": 2,
            "Refus": 5,
            "Recrutement": 1,
        },
        "recrutements_finalises": [reference_finalisee],
        "notes": 3,
        "conversations": 1,
        "messages": 2,
        "reponses_candidat": 1,
        "lectures": 2,
    }


def _organisme_avec_agents():
    organisme = OrganismeDjangoFactory()
    OrganismeAgentDjangoFactory(
        organisme=organisme, role=AgentOrganismeRole.SUPERVISEUR.value
    )
    OrganismeAgentDjangoFactory(organisme=organisme)
    return organisme


def _seed(*options, stdout=None):
    call_command("seed_demo_organisme", *options, stdout=stdout or StringIO())


def _candidatures_demo(organisme_id):
    return CandidatureModel.objects.filter(
        etape__recrutement__organisme_id=organisme_id,
        etape__recrutement__offre__source_id=SOURCE_DEMO_ID,
    )


def _comptes(organisme_id):
    candidatures = _candidatures_demo(organisme_id)
    recrutements = RecrutementModel.objects.filter(
        organisme_id=organisme_id, offre__source_id=SOURCE_DEMO_ID
    )
    return {
        "offres": OfferModel.objects.filter(recrutement__in=recrutements).count(),
        "recrutements_en_cours": recrutements.filter(
            offre__archived_at__isnull=True
        ).count(),
        "recrutements_archives": recrutements.filter(
            offre__archived_at__isnull=False
        ).count(),
        "responsables": RecrutementAgentModel.objects.filter(
            recrutement__in=recrutements,
            role=AgentRecrutementRole.RESPONSABLE.value,
        ).count(),
        "candidatures": candidatures.count(),
        "candidats": UserModel.objects.filter(
            email__endswith="@demo.candidat.fr",
            profil_candidat__candidatures__in=candidatures,
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


def _identites(organisme_id):
    return sorted(
        UserModel.objects.filter(
            profil_candidat__candidatures__in=_candidatures_demo(organisme_id)
        ).values_list("first_name", "last_name", "email")
    )


def _rien_ecrit():
    assert not OfferModel.objects.filter(source_id=SOURCE_DEMO_ID).exists()
    assert not SourceModel.objects.filter(source_id=SOURCE_DEMO_ID).exists()
    assert not UserModel.objects.filter(email__endswith="@demo.candidat.fr").exists()


class TestSeedDemoOrganisme:
    def test_seeds_each_organisme_and_force_only_removes_its_own(self, db):
        organisme_a = _organisme_avec_agents()
        organisme_b = _organisme_avec_agents()
        _, candidature_a = create_recrutement_with_candidature(organisme=organisme_a)
        _, candidature_ailleurs = create_recrutement_with_candidature()
        cibles = [(organisme_a.pk, SPEC_A), (organisme_b.pk, SPEC_B)]

        resultat = seed_demo_organisme(cibles)

        assert [o["status"] for o in resultat["organismes"]] == ["seeded", "seeded"]
        assert _comptes(organisme_a.pk) == _comptes_reduits("DEMO-a-02")
        assert _comptes(organisme_b.pk) == _comptes_reduits("DEMO-b-02")
        identites_a, identites_b = (
            _identites(organisme_a.pk),
            _identites(organisme_b.pk),
        )
        assert [nom for *nom, _ in identites_a] != [nom for *nom, _ in identites_b]
        assert not {e for *_, e in identites_a} & {e for *_, e in identites_b}
        candidatures = CandidatureModel.objects.filter(
            etape__recrutement__offre__source_id=SOURCE_DEMO_ID
        )
        assert not candidatures.filter(
            created_at__lt=F("etape__recrutement__offre__publication_date")
        ).exists()
        assert not MessageModel.objects.filter(
            conversation__candidature__in=candidatures,
            created_at__lt=F("conversation__candidature__created_at"),
        ).exists()
        note = NoteModel.objects.filter(candidature__in=candidatures).first()
        lignes = note.message.splitlines()  # type: ignore[union-attr]
        assert (lignes[0], len(lignes)) == ("Compte rendu de présélection", 16)
        candidature_etat = candidatures.filter(
            etape__recrutement__offre__reference="DEMO-a-01"
        ).first()
        cv = DocumentModel.objects.get(candidature=candidature_etat)
        with cv.fichier.open("rb") as fichier:
            texte = "".join(
                page.extract_text() for page in PdfReader(BytesIO(fichier.read())).pages
            )
        nom_complet = candidature_etat.candidat.utilisateur.get_full_name()  # type: ignore[union-attr]
        assert nom_complet in texte
        assert "l’État" in texte
        assert nom_complet in candidature_etat.candidat.resume  # type: ignore[union-attr]
        avec_avatar = set()
        for candidature in candidatures.select_related(
            "candidat__utilisateur", "etape__recrutement__offre"
        ):
            utilisateur = candidature.candidat.utilisateur
            cv = DocumentModel.objects.get(candidature=candidature)
            with cv.fichier.open("rb") as fichier:
                premiere_page = PdfReader(BytesIO(fichier.read())).pages[0]
            initiales = f"{utilisateur.first_name[0]}{utilisateur.last_name[0]}"
            avec_avatar.add(
                premiere_page.extract_text().split()[0] == initiales.upper()
            )
            reference = candidature.etape.recrutement.offre.reference
            famille = _RECRUTEMENTS_REDUITS[int(reference[-2:]) - 1]["famille"]
            assert any(
                f"{experience['titre']}, {experience['employeur']}"
                in candidature.candidat.resume
                for experience in CORPUS[famille]["experiences_directes"]
            )
        assert avec_avatar == {True, False}

        simulation = seed_demo_organisme(cibles, dry_run=True)
        assert [o["a_supprimer"] for o in simulation["organismes"]] == [
            {"offres": 3, "candidatures": 13, "candidats": 13},
            {"offres": 3, "candidatures": 13, "candidats": 13},
        ]

        rejeu = seed_demo_organisme(cibles)

        assert [o["status"] for o in rejeu["organismes"]] == [
            "already_seeded",
            "already_seeded",
        ]
        assert _identites(organisme_a.pk) == identites_a

        seed_demo_organisme([(organisme_a.pk, SPEC_A)], force=True)

        assert _comptes(organisme_a.pk) == _comptes_reduits("DEMO-a-02")
        assert _comptes(organisme_b.pk) == _comptes_reduits("DEMO-b-02")
        assert _identites(organisme_a.pk) == identites_a
        assert _identites(organisme_b.pk) == identites_b
        assert set(
            CandidatureModel.objects.filter(
                pk__in=[candidature_a.pk, candidature_ailleurs.pk]
            ).values_list("pk", flat=True)
        ) == {candidature_a.pk, candidature_ailleurs.pk}

    @pytest.mark.parametrize(
        ("cas", "motif"),
        [
            ("organisme_absent", "introuvable ou supprimé"),
            ("organisme_supprime", "introuvable ou supprimé"),
            ("aucun_agent_actif", "aucun agent actif"),
            ("production", "production"),
            ("cle_inconnue", "clé d'organisme inconnue : inconnue"),
        ],
    )
    def test_stops_without_writing(self, db, monkeypatch, cas, motif):
        autre = _organisme_avec_agents()
        cle = "culture"
        cible_id = uuid4()
        if cas == "organisme_supprime":
            cible_id = OrganismeAgentDjangoFactory(
                organisme=OrganismeDjangoFactory(supprime_le=timezone.now())
            ).organisme_id
        elif cas == "aucun_agent_actif":
            cible_id = OrganismeAgentDjangoFactory(
                date_revocation=timezone.now()
            ).organisme_id
        elif cas == "production":
            cible_id = _organisme_avec_agents().pk
            monkeypatch.setenv("SCALEWAY_ENV", "prod")
        elif cas == "cle_inconnue":
            cible_id = _organisme_avec_agents().pk
            cle = "inconnue"

        with pytest.raises(CommandError, match=motif):
            _seed(
                "--organisme",
                f"culture={autre.pk}",
                "--organisme",
                f"{cle}={cible_id}",
                "--force",
            )

        _rien_ecrit()

    def test_dry_run_prints_the_full_spec_without_writing(self, db):
        organismes = {cle: _organisme_avec_agents() for cle in CLES_DEMO}
        sortie = StringIO()

        _seed(
            *[
                option
                for cle, organisme in organismes.items()
                for option in ("--organisme", f"{cle}={organisme.pk}")
            ],
            "--dry-run",
            stdout=sortie,
        )

        blocs = [bloc.splitlines() for bloc in sortie.getvalue().split("== ")[1:]]
        assert [bloc[0] for bloc in blocs] == [
            f"{cle} ({organisme.pk})" for cle, organisme in organismes.items()
        ]
        for bloc in blocs:
            assert bloc[1:10] == [
                "À supprimer avec --force : 0 offres, 0 candidatures, 0 candidats.",
                "Offres : 15 (10 en cours, 5 archivées).",
                "Candidatures : 683.",
                "  Réception des candidatures : 293",
                "  Présélection : 111",
                "  Entretien : 62",
                "  Proposition : 27",
                "  Refus : 187",
                "  Recrutement : 3",
            ]
        _rien_ecrit()

    @pytest.mark.parametrize(
        "famille",
        # miroir de Famille au 27/10
        [
            "pilotage",
            "rh",
            "juridique",
            "finances",
            "achats",
            "numerique",
            "communication",
            "culture",
            "audit",
            "environnement",
            "solidarites",
        ],
    )
    def test_generates_a_pdf_cv_for_each_famille(self, famille):
        # miroir des bornes de _APPRECIATIONS au 27/10
        for proximite in (0.4, 0.9):
            candidature = _CandidaturePlan(
                etape="Présélection",
                prenom="Camille",
                nom="Durand",
                proximite=proximite,
                note=False,
                conversation=False,
                lecture=False,
                avatar=None,
            )

            cv = _cv(
                random.Random(0),
                CORPUS[famille],
                candidature,
                "camille.durand@demo.candidat.fr",
            )

            pdf = PdfReader(BytesIO(_pdf_texte(cv.lignes, None)))
            assert "Camille Durand" in "".join(p.extract_text() for p in pdf.pages)
