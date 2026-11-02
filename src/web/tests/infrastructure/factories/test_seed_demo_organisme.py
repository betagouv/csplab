import random
from datetime import datetime
from io import BytesIO, StringIO
from uuid import UUID, uuid4

import pytest
from django.core.management import CommandError, call_command
from django.db.models import Count, F, Min
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
    _au_poste,
    _CandidaturePlan,
    _cv,
    _pdf_texte,
    seed_demo_organisme,
)
from infrastructure.factories.seed_demo_specs import RecrutementSpec, SpecOrganisme

# miroir de _SOURCE_DEMO_UUID au 27/10
SOURCE_DEMO_ID = UUID("00000000-0000-0000-0000-000000001945")

# miroir de SPECS_DEMO au 29/10
CLES_DEMO = [
    "transition-ecologique",
    "culture",
    "centre-pompidou",
    "premier-ministre",
    "cour-des-comptes",
    "travail-solidarites",
    "dgafp",
    "economie-finances",
    "caisse-des-depots",
]

_RECRUTEMENTS_REDUITS: list[RecrutementSpec] = [
    {
        "intitule": "Conseiller(ère) finances et garanties de l’État",
        "famille": "finances",
        "archive_depuis_jours": None,
        "repartition": (2, 1, 1, 1, 1, 0),
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
        "candidatures": 14,
        "candidats": 14,
        "cvs": 14,
        "par_etape": {
            "Réception des candidatures": 3,
            "Présélection": 2,
            "Entretien": 2,
            "Proposition": 1,
            "Refus": 5,
            "Recrutement": 1,
        },
        "recrutements_finalises": [reference_finalisee],
        "notes": 6,
        "conversations": {
            "Date d’entretien": 2,
            "Demande de pièces justificatives": 2,
        },
        "messages": 8,
        "reponses_candidat": 4,
        "lectures": 8,
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
        "conversations": dict(
            ConversationModel.objects.filter(candidature__in=candidatures)
            .values("objet")
            .annotate(n=Count("id"))
            .values_list("objet", "n")
        ),
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


def _notes(organisme_id):
    return sorted(
        NoteModel.objects.filter(
            candidature__in=_candidatures_demo(organisme_id)
        ).values_list("message", flat=True)
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
        notes_a = _notes(organisme_a.pk)
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
            {"offres": 3, "candidatures": 14, "candidats": 14},
            {"offres": 3, "candidatures": 14, "candidats": 14},
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
        assert _notes(organisme_a.pk) == notes_a
        assert set(
            CandidatureModel.objects.filter(
                pk__in=[candidature_a.pk, candidature_ailleurs.pk]
            ).values_list("pk", flat=True)
        ) == {candidature_a.pk, candidature_ailleurs.pk}

    def test_seeds_ticket_note_templates_with_coherent_dates_and_authors(self, db):
        organisme = _organisme_avec_agents()

        seed_demo_organisme([(organisme.pk, SPEC_A)])

        notes = NoteModel.objects.filter(
            candidature__in=_candidatures_demo(organisme.pk)
        ).select_related("candidature__candidat", "candidature__etape")
        en_tetes: dict[str, set[str]] = {}
        for note in notes:
            lignes = note.message.splitlines()
            en_tetes.setdefault(note.candidature.etape.nom, set()).add(lignes[0])
            jour = timezone.localtime(note.created_at).strftime("%d/%m/%Y")
            assert lignes[1].startswith(
                (f"Date de l'appel : {jour}", f"Entretien du {jour} – ")
            )
            if lignes[0] == "Compte rendu d'entretien":
                parcours = lignes[lignes.index("Parcours") + 1]
                experience = parcours.split(" comme ", 1)[1]
                assert experience in note.candidature.candidat.resume
        assert en_tetes == {
            "Présélection": {"Premier appel"},
            "Entretien": {"Compte rendu d'entretien"},
            "Recrutement": {"Premier appel", "Compte rendu d'entretien"},
        }
        retenue = notes.filter(candidature__etape__nom="Recrutement")
        auteurs = set(retenue.values_list("publie_par_id", flat=True))
        assert len(auteurs) == retenue.count()
        assert not notes.filter(created_at__lt=F("candidature__created_at")).exists()
        assert not notes.filter(
            created_at__gt=F("candidature__etape__recrutement__offre__archived_at")
        ).exists()
        comptes_rendus_avec_fil = (
            notes.filter(message__startswith="Compte rendu d'entretien")
            .annotate(
                demande_le=Min("candidature__conversations__messages__created_at")
            )
            .filter(demande_le__isnull=False)
        )
        assert sorted(
            comptes_rendus_avec_fil.values_list("candidature__etape__nom", flat=True)
        ) == ["Entretien", "Recrutement"]
        assert not comptes_rendus_avec_fil.filter(
            created_at__gte=F("demande_le")
        ).exists()

    def test_seeds_ticket_conversations_each_answered_by_the_candidate(self, db):
        organisme = _organisme_avec_agents()

        seed_demo_organisme([(organisme.pk, SPEC_A)])

        conversations = ConversationModel.objects.filter(
            candidature__in=_candidatures_demo(organisme.pk)
        ).select_related("candidature__etape__recrutement__offre")
        objets: dict[str, set[str]] = {}
        fils_retenue = {}
        for conversation in conversations:
            candidature = conversation.candidature
            offre = candidature.etape.recrutement.offre
            messages = list(conversation.messages.order_by("created_at"))
            objets.setdefault(candidature.etape.nom, set()).add(conversation.objet)
            assert [m.auteur_id == candidature.candidat_id for m in messages] == [
                False,
                True,
            ]
            if offre.archived_at is not None:
                assert messages[-1].created_at < offre.archived_at
            if conversation.objet == "Demande de pièces justificatives":
                demande = messages[0]
                limite = demande.contenu.split("avant le ", 1)[1][:10]
                assert f"au poste de {offre.title}." in demande.contenu
                assert (
                    datetime.strptime(limite, "%d/%m/%Y").date()
                    > timezone.localtime(demande.created_at).date()
                )
            if candidature.etape.nom == "Recrutement":
                fils_retenue[conversation.objet] = messages
        assert objets == {
            "Entretien": {"Date d’entretien"},
            "Proposition": {"Demande de pièces justificatives"},
            "Recrutement": {"Date d’entretien", "Demande de pièces justificatives"},
        }
        assert (
            fils_retenue["Date d’entretien"][-1].created_at
            < fils_retenue["Demande de pièces justificatives"][0].created_at
        )
        retenue = conversations.filter(candidature__etape__nom="Recrutement")
        equipe = RecrutementAgentModel.objects.filter(
            recrutement=retenue.first().candidature.etape.recrutement
        ).values_list("agent__utilisateur_id", flat=True)
        assert [retenue.unread_by(agent).count() for agent in equipe] == [0, 0]

    @pytest.mark.parametrize(
        ("intitule", "attendu"),
        [
            ("Attaché(e) de presse", "au poste d'Attaché(e) de presse"),
            ("Économiste", "au poste d'Économiste"),
            ("Chargé(e) de recrutement", "au poste de Chargé(e) de recrutement"),
        ],
    )
    def test_elides_au_poste_de_before_a_vowel(self, intitule, attendu):
        assert _au_poste(intitule) == attendu

    @pytest.mark.parametrize(
        ("cas", "motif"),
        [
            ("organisme_absent", "introuvable ou supprimé"),
            ("organisme_supprime", "introuvable ou supprimé"),
            ("aucun_agent_actif", "aucun agent actif"),
            ("production", "production"),
            ("cle_inconnue", "clé d'organisme inconnue : inconnue"),
            ("sans_egal", "format attendu : CLE=UUID"),
            ("uuid_invalide", "UUID d'organisme invalide : pas-un-uuid"),
            ("cle_en_double", "qu'une fois dans --organisme"),
            ("organisme_en_double", "qu'une fois dans --organisme"),
        ],
    )
    def test_stops_without_writing(self, db, monkeypatch, cas, motif):
        autre = _organisme_avec_agents()
        cle = "dgafp"
        cible_id = uuid4()
        cible: str | None = None
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
        elif cas == "sans_egal":
            cible = str(_organisme_avec_agents().pk)
        elif cas == "uuid_invalide":
            cible = "dgafp=pas-un-uuid"
        elif cas == "cle_en_double":
            cle, cible_id = "culture", _organisme_avec_agents().pk
        elif cas == "organisme_en_double":
            cible_id = autre.pk

        with pytest.raises(CommandError, match=motif):
            _seed(
                "--organisme",
                f"culture={autre.pk}",
                "--organisme",
                cible or f"{cle}={cible_id}",
                "--force",
            )

        _rien_ecrit()

    def test_refuses_a_cle_already_seeded_on_another_organisme(self, db):
        premier, second = _organisme_avec_agents(), _organisme_avec_agents()
        seed_demo_organisme(
            [
                (
                    premier.pk,
                    SpecOrganisme(
                        cle="culture", graine=1, recrutements=_RECRUTEMENTS_REDUITS
                    ),
                )
            ]
        )

        with pytest.raises(CommandError, match="déjà semée sur un autre organisme"):
            _seed("--organisme", f"culture={second.pk}", "--force")

        assert _comptes(premier.pk) == _comptes_reduits("DEMO-culture-02")
        assert not _candidatures_demo(second.pk).exists()

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
            assert bloc[10] == "Notes : 98, conversations : 52 (dont 29 lues)."
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
        # miroir des bornes de _AVIS au 27/10
        for proximite in (0.4, 0.9):
            candidature = _CandidaturePlan(
                etape="Présélection",
                prenom="Camille",
                nom="Durand",
                proximite=proximite,
                notes=(),
                fils=(),
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

    def test_direct_experiences_are_not_always_listed_first(self):
        candidature = _CandidaturePlan(
            etape="Présélection",
            prenom="Camille",
            nom="Durand",
            proximite=0.4,
            notes=(),
            fils=(),
            lecture=False,
            avatar=None,
        )

        premiere_directe = {
            _cv(
                random.Random(graine),
                CORPUS["finances"],
                candidature,
                "camille.durand@demo.candidat.fr",
            ).experiences[0][1]
            in CORPUS["finances"]["experiences_directes"]
            for graine in range(10)
        }

        assert premiere_directe == {True, False}
