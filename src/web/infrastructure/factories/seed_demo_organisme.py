import os
import random
import textwrap
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from itertools import cycle
from typing import TypedDict
from uuid import UUID

import factory.random
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.text import slugify
from faker import Faker

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    ConversationLectureDjangoFactory,
    MessageDjangoFactory,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.factories.seed_demo_cv_corpus import (
    CORPUS,
    LANGUES,
    NOTE_LIGNES,
    VILLES,
    PosteCorpus,
)
from infrastructure.factories.seed_recruteur_datas import delete_candidatures

_SEED = 1945
_REFERENCE_PREFIX = "DEMO-1945-"
_EMAIL_DOMAIN = "@demo.candidat.fr"
_SOURCE_DEMO_UUID = UUID("00000000-0000-0000-0000-000000001945")
_SOURCE_DEMO_SLUG = "demo-1945"

_RECEPTION = "Réception des candidatures"
_PRESELECTION = "Présélection"
_ENTRETIEN = "Entretien"
_PROPOSITION = "Proposition"
_REFUS = "Refus"
_RECRUTEMENT = "Recrutement"
_ETAPES = (_RECEPTION, _PRESELECTION, _ENTRETIEN, _PROPOSITION, _REFUS, _RECRUTEMENT)
_ETAPES_AVEC_NOTE = (_PRESELECTION, _ENTRETIEN, _PROPOSITION, _RECRUTEMENT)


class _RecrutementSpec(TypedDict):
    reference: str
    intitule: str
    archive_depuis_jours: int | None
    repartition: tuple[int, int, int, int, int, int]


# repartition : candidatures par étape, dans l'ordre de _ETAPES.
_RECRUTEMENTS_SPECS: list[_RecrutementSpec] = [
    {
        "reference": "DEMO-1945-001",
        "intitule": "Secrétaire général(e)",
        "archive_depuis_jours": None,
        "repartition": (52, 19, 9, 5, 9, 0),
    },
    {
        "reference": "DEMO-1945-002",
        "intitule": "Conseiller(ère) héritage",
        "archive_depuis_jours": None,
        "repartition": (0, 0, 0, 0, 0, 0),
    },
    {
        "reference": "DEMO-1945-003",
        "intitule": "Chargé(e) de mission infrastructures",
        "archive_depuis_jours": None,
        "repartition": (2, 1, 1, 0, 1, 0),
    },
    {
        "reference": "DEMO-1945-004",
        "intitule": "Conseiller(ère) juridique / affaires législatives",
        "archive_depuis_jours": None,
        "repartition": (37, 13, 7, 3, 7, 0),
    },
    {
        "reference": "DEMO-1945-005",
        "intitule": "Conseiller(ère) finances et garanties de l’État",
        "archive_depuis_jours": None,
        "repartition": (2, 1, 1, 0, 1, 0),
    },
    {
        "reference": "DEMO-1945-006",
        "intitule": "Conseiller(ère) sécurité et ordre public",
        "archive_depuis_jours": None,
        "repartition": (27, 10, 5, 2, 4, 0),
    },
    {
        "reference": "DEMO-1945-007",
        "intitule": "Conseiller(ère) transports et mobilités",
        "archive_depuis_jours": None,
        "repartition": (18, 6, 3, 2, 3, 0),
    },
    {
        "reference": "DEMO-1945-008",
        "intitule": "Chargé(e) de mission relations territoriales",
        "archive_depuis_jours": None,
        "repartition": (2, 1, 1, 0, 1, 0),
    },
    {
        "reference": "DEMO-1945-009",
        "intitule": "Chargé(e) de mission relations territoriales",
        "archive_depuis_jours": 20,
        "repartition": (1, 0, 2, 1, 7, 1),
    },
    {
        "reference": "DEMO-1945-010",
        "intitule": "Chargé(e) de mission transition écologique et sobriété",
        "archive_depuis_jours": 45,
        "repartition": (1, 0, 3, 1, 10, 1),
    },
    {
        "reference": "DEMO-1945-011",
        "intitule": "Chargé(e) de mission accessibilité et Jeux paralympiques",
        "archive_depuis_jours": 90,
        "repartition": (2, 0, 3, 2, 11, 1),
    },
]

_SAMEDI = 5
_CRENEAUX = ((3, "10 h"), (5, "14 h 30"), (8, "11 h"))
_CANDIDATURES_ETALEES_SUR = timedelta(days=30)
_DEMANDE_ENVOYEE_A = time(9, 30)
_REPONSE_ENVOYEE_A = time(16, 30)


@dataclass
class _CandidaturePlan:
    etape: str
    prenom: str
    nom: str
    proximite: float
    note: bool
    conversation: bool
    lecture: bool


@dataclass
class _RecrutementPlan:
    spec: _RecrutementSpec
    candidatures: list[_CandidaturePlan]


@dataclass
class _Cv:
    lignes: list[tuple[str, bool]]
    experience: str
    competence: str


def _planifier(fake: Faker, rng: random.Random) -> list[_RecrutementPlan]:
    plans = []
    nb_conversations = 0
    for spec in _RECRUTEMENTS_SPECS:
        candidatures = []
        nb_suivies = 0
        for etape, nombre in zip(_ETAPES, spec["repartition"], strict=True):
            for _ in range(nombre):
                note = False
                if etape in _ETAPES_AVEC_NOTE:
                    note = nb_suivies % 3 == 0
                    nb_suivies += 1
                conversation = (
                    etape == _ENTRETIEN and spec["archive_depuis_jours"] is None
                )
                lecture = False
                if conversation:
                    lecture = nb_conversations % 2 == 0
                    nb_conversations += 1
                candidatures.append(
                    _CandidaturePlan(
                        etape=etape,
                        prenom=fake.first_name(),
                        nom=fake.last_name(),
                        proximite=rng.random(),
                        note=note,
                        conversation=conversation,
                        lecture=lecture,
                    )
                )
        plans.append(_RecrutementPlan(spec=spec, candidatures=candidatures))
    return plans


def _comptes(plans: list[_RecrutementPlan]) -> dict:
    candidatures = [c for plan in plans for c in plan.candidatures]
    return {
        "offres": len(plans),
        "recrutements_en_cours": sum(
            plan.spec["archive_depuis_jours"] is None for plan in plans
        ),
        "recrutements_archives": sum(
            plan.spec["archive_depuis_jours"] is not None for plan in plans
        ),
        "candidatures": len(candidatures),
        "par_etape": {
            etape: sum(c.etape == etape for c in candidatures) for etape in _ETAPES
        },
        "notes": sum(c.note for c in candidatures),
        "conversations": sum(c.conversation for c in candidatures),
        "conversations_lues": sum(c.lecture for c in candidatures),
    }


def _offres_demo():
    return OfferModel.objects.filter(reference__startswith=_REFERENCE_PREFIX)


def _candidatures_demo():
    return CandidatureModel.objects.filter(
        Q(etape__recrutement__offre__reference__startswith=_REFERENCE_PREFIX)
        | Q(candidat__utilisateur__email__endswith=_EMAIL_DOMAIN)
    )


def _a_supprimer() -> dict:
    return {
        "offres": _offres_demo().count(),
        "candidatures": _candidatures_demo().count(),
        "candidats": UserModel.objects.filter(email__endswith=_EMAIL_DOMAIN).count(),
    }


def _supprimer_demo() -> None:
    delete_candidatures(list(_candidatures_demo().values_list("id", flat=True)))
    RecrutementModel.objects.filter(offre__in=_offres_demo()).delete()
    _offres_demo().delete()
    ProfilCandidatModel.objects.filter(
        utilisateur__email__endswith=_EMAIL_DOMAIN
    ).delete()
    UserModel.objects.filter(email__endswith=_EMAIL_DOMAIN).delete()
    SourceModel.objects.filter(source_id=_SOURCE_DEMO_UUID).delete()


def _echapper(texte: str) -> bytes:
    return (
        texte.encode("cp1252")
        .replace(b"\\", b"\\\\")
        .replace(b"(", b"\\(")
        .replace(b")", b"\\)")
    )


_PAGE = (595, 842)
_MARGE = 56
_INTERLIGNE = 13
_LIGNES_PAR_PAGE = (_PAGE[1] - 2 * _MARGE) // _INTERLIGNE
_CARACTERES_PAR_LIGNE = 90


def _flux_page(lignes: list[tuple[str, bool]]) -> bytes:
    morceaux = [
        b"BT",
        b"%d TL" % _INTERLIGNE,
        b"%d %d Td" % (_MARGE, _PAGE[1] - _MARGE),
    ]
    police = b""
    for texte, gras in lignes:
        voulue = b"/F2" if gras else b"/F1"
        if voulue != police:
            morceaux.append(voulue + b" 10 Tf")
            police = voulue
        morceaux.append(b"(" + _echapper(texte) + b") Tj T*")
    morceaux.append(b"ET")
    return b"\n".join(morceaux)


def _pdf_texte(lignes: list[tuple[str, bool]]) -> bytes:
    coupees = [
        (morceau, gras)
        for texte, gras in lignes
        for morceau in textwrap.wrap(texte, width=_CARACTERES_PAR_LIGNE) or [""]
    ]
    pages = [
        coupees[debut : debut + _LIGNES_PAR_PAGE]
        for debut in range(0, len(coupees), _LIGNES_PAR_PAGE)
    ] or [[]]
    pages_ids = [5 + 2 * rang for rang in range(len(pages))]
    objets = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [%s] /Count %d >>"
        % (b" ".join(b"%d 0 R" % page_id for page_id in pages_ids), len(pages)),
        (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>"
        ),
        (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
            b"/Encoding /WinAnsiEncoding >>"
        ),
    ]
    for page_id, page in zip(pages_ids, pages, strict=True):
        flux = _flux_page(page)
        objets.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
            b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            b"/Contents %d 0 R >>" % (_PAGE[0], _PAGE[1], page_id + 1)
        )
        objets.append(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(flux), flux))
    sortie = bytearray(b"%PDF-1.4\n")
    positions = []
    for numero, corps in enumerate(objets, start=1):
        positions.append(len(sortie))
        sortie += b"%d 0 obj\n%s\nendobj\n" % (numero, corps)
    debut_xref = len(sortie)
    sortie += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objets) + 1)
    for position in positions:
        sortie += b"%010d 00000 n \n" % position
    sortie += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objets) + 1,
        debut_xref,
    )
    return bytes(sortie)


def _cv(
    rng: random.Random,
    corpus: PosteCorpus,
    candidature: _CandidaturePlan,
    email: str,
) -> _Cv:
    nb_directes = round(candidature.proximite * 3)
    nb_competences_poste = 1 + round(candidature.proximite * 4)
    experiences = rng.sample(corpus["experiences_directes"], nb_directes) + rng.sample(
        corpus["experiences_voisines"], 3 - nb_directes
    )
    competences = rng.sample(
        corpus["competences_poste"], nb_competences_poste
    ) + rng.sample(corpus["competences_voisines"], 6 - nb_competences_poste)

    lignes: list[tuple[str, bool]] = [
        (f"{candidature.prenom} {candidature.nom}", True),
        (f"{email} - {rng.choice(VILLES)}", False),
        ("", False),
        ("Profil", True),
        (rng.choice(corpus["profil"]), False),
        ("", False),
        ("Expériences professionnelles", True),
    ]
    fin = 2026
    for experience in experiences:
        debut = fin - rng.randint(2, 4)
        lignes.append(
            (
                f"{debut} - {fin} : {experience['titre']}, {experience['employeur']}",
                True,
            )
        )
        lignes.append((experience["description"], False))
        fin = debut
    lignes += [("", False), ("Formation", True)]
    annee = fin - rng.randint(0, 1)
    for formation in rng.sample(corpus["formations"], 2):
        lignes.append(
            (f"{annee} : {formation['diplome']}, {formation['etablissement']}", False)
        )
        annee -= rng.randint(2, 3)
    lignes += [("", False), ("Compétences", True)]
    lignes += [(f"- {competence}", False) for competence in competences]
    lignes += [("", False), ("Langues", True), (rng.choice(LANGUES), False)]
    return _Cv(
        lignes=lignes,
        experience=f"{experiences[0]['titre']}, {experiences[0]['employeur']}",
        competence=competences[0],
    )


def _appreciation(proximite: float) -> str:
    if proximite >= 2 / 3:
        return "Parcours en adéquation directe avec les missions du poste."
    if proximite >= 1 / 3:
        return "Parcours en partie aligné sur le poste, expériences voisines utiles."
    return "Parcours voisin du poste, adéquation à confirmer en entretien."


def _note(candidature: _CandidaturePlan, intitule: str, cv: _Cv) -> str:
    return "\n".join(
        [
            "Compte rendu de présélection",
            *(
                ligne.format(
                    prenom=candidature.prenom,
                    nom=candidature.nom,
                    intitule=intitule,
                    experience=cv.experience,
                    competence=cv.competence,
                    appreciation=_appreciation(candidature.proximite),
                )
                for ligne in NOTE_LIGNES
            ),
        ]
    )


def _jours_ouvres(depuis: date, rangs: list[int], pas: int = 1) -> dict[int, date]:
    jours: dict[int, date] = {}
    jour, rang = depuis, 0
    while len(jours) < len(rangs):
        jour += timedelta(days=pas)
        if jour.weekday() < _SAMEDI:
            rang += 1
            if rang in rangs:
                jours[rang] = jour
    return jours


def _creneau(jour: date, heure: str) -> str:
    quantieme = "1er" if jour.day == 1 else str(jour.day)
    return f"{date_format(jour, 'l')} {quantieme} {date_format(jour, 'F')} à {heure}"


def _seed_conversation(
    candidature: CandidatureModel,
    plan: _CandidaturePlan,
    recruteur: UserModel,
    creneaux: list[str],
    choix: int,
    envois: tuple[datetime, datetime],
) -> None:
    conversation = ConversationDjangoFactory.create(
        candidature=candidature, objet="Date d’entretien"
    )
    candidat = candidature.candidat.utilisateur
    lignes_creneaux = "\n".join(f"- {creneau}" for creneau in creneaux)
    demande = MessageDjangoFactory.create(
        conversation=conversation,
        auteur=recruteur,
        contenu=(
            f"Bonjour {plan.prenom},\n\n"
            "Quelles sont vos disponibilités pour un entretien sur les 3 "
            f"créneaux suivants :\n{lignes_creneaux}\n\n"
            f"Bien cordialement,\n{recruteur.get_full_name()}"
        ),
    )
    reponse = MessageDjangoFactory.create(
        conversation=conversation,
        auteur=candidat,
        contenu=(
            f"Bonjour {recruteur.first_name},\n\n"
            f"Je suis disponible le {creneaux[choix]}.\n\n"
            f"Cordialement,\n{plan.prenom} {plan.nom}"
        ),
    )
    demande_le, lu_le = envois
    MessageModel.objects.filter(pk=demande.pk).update(created_at=demande_le)
    MessageModel.objects.filter(pk=reponse.pk).update(created_at=lu_le)
    if plan.lecture:
        for lecteur in (recruteur, candidat):
            ConversationLectureDjangoFactory.create(
                conversation=conversation, utilisateur=lecteur, read_at=lu_le
            )


def _seed_cv(candidature: CandidatureModel, utilisateur: UserModel, pdf: bytes) -> None:
    nom_original = f"CV {utilisateur.get_full_name()}.pdf"
    DocumentDjangoFactory(
        candidature=candidature,
        type_document=TypeDocument.CV.value,
        fichier=ContentFile(pdf, name=nom_original),
        nom_original=nom_original,
        content_type="application/pdf",
        taille=len(pdf),
        depose_par=utilisateur,
    )


def _seed_recrutement(
    spec: _RecrutementSpec,
    organisme: OrganismeModel,
    source: SourceModel,
    responsable: ProfilAgentModel,
    maintenant: datetime,
) -> RecrutementModel:
    corpus = CORPUS[spec["intitule"]]
    offre = {
        "source": source,
        "reference": spec["reference"],
        "title": spec["intitule"],
        "organization": organisme.nom,
        "mission": corpus["mission"],
        "profile": corpus["profil_recherche"],
    }
    responsable_kwargs = {
        "organisme": organisme,
        "agent_link__agent": responsable,
        "agent_link__role": AgentRecrutementRole.RESPONSABLE.value,
    }
    if spec["archive_depuis_jours"] is None:
        return RecrutementDjangoFactory(  # type: ignore[return-value]
            offre=OfferDjangoFactory(
                publication_date=maintenant - _CANDIDATURES_ETALEES_SUR, **offre
            ),
            **responsable_kwargs,
        )
    archive_le = maintenant - timedelta(days=spec["archive_depuis_jours"])
    return RecrutementDjangoFactory(  # type: ignore[return-value]
        offre_archivee=True,
        offre__archived_at=archive_le,
        offre__publication_date=archive_le - _CANDIDATURES_ETALEES_SUR,
        **{f"offre__{champ}": valeur for champ, valeur in offre.items()},
        **responsable_kwargs,
    )


class _SeedRefuse(Exception):
    def __init__(self, status: str, **contexte) -> None:
        super().__init__(status)
        self.contexte = {"status": status, **contexte}


def _cible(organisme_id: UUID) -> tuple[OrganismeModel, list[ProfilAgentModel]]:
    if os.environ.get("SCALEWAY_ENV") == "prod":
        raise _SeedRefuse("production")
    organisme = OrganismeModel.objects.by_id(organisme_id).first()
    if organisme is None:
        raise _SeedRefuse("organisme_absent")
    agents = [
        liaison.agent
        for liaison in OrganismeAgentModel.objects.active()
        .filter(organisme_id=organisme.pk)
        .select_related("agent__utilisateur")
        .order_by("created_at")
    ]
    if not agents:
        raise _SeedRefuse("aucun_agent_actif")
    autre_organisme_id = (
        RecrutementModel.objects.filter(offre__in=_offres_demo())
        .exclude(organisme_id=organisme.pk)
        .values_list("organisme_id", flat=True)
        .first()
    )
    if autre_organisme_id is not None:
        raise _SeedRefuse("deja_seede_ailleurs", autre_organisme_id=autre_organisme_id)
    return organisme, agents


def _ecrire(
    plans: list[_RecrutementPlan],
    organisme: OrganismeModel,
    agents: list[ProfilAgentModel],
    fake: Faker,
    rng: random.Random,
) -> None:
    maintenant = timezone.now()
    jours = _jours_ouvres(timezone.localdate(), [rang for rang, _ in _CRENEAUX])
    creneaux = [_creneau(jours[rang], heure) for rang, heure in _CRENEAUX]
    jours_passes = _jours_ouvres(timezone.localdate(), [1, 2], pas=-1)
    envois = (
        timezone.make_aware(datetime.combine(jours_passes[2], _DEMANDE_ENVOYEE_A)),
        timezone.make_aware(datetime.combine(jours_passes[1], _REPONSE_ENVOYEE_A)),
    )
    motifs_refus = cycle(MotifRefus.values)
    responsables = cycle(agents)
    candidatures_creees: list[CandidatureModel] = []
    nb_conversations = 0

    source: SourceModel = SourceDjangoFactory(  # type: ignore[assignment]
        source_id=_SOURCE_DEMO_UUID, slug=_SOURCE_DEMO_SLUG
    )
    for plan in plans:
        spec = plan.spec
        responsable = next(responsables)
        recrutement = _seed_recrutement(
            spec, organisme, source, responsable, maintenant
        )
        for agent in agents:
            if agent.pk != responsable.pk:
                RecrutementAgentDjangoFactory(
                    recrutement=recrutement,
                    agent=agent,
                    role=AgentRecrutementRole.CONTRIBUTEUR.value,
                )
        etapes = {etape.nom: etape for etape in recrutement.etapes.all()}  # type: ignore[attr-defined]
        fin = maintenant
        if spec["archive_depuis_jours"] is not None:
            fin = maintenant - timedelta(days=spec["archive_depuis_jours"])
        for candidature_plan in plan.candidatures:
            email = (
                f"{slugify(candidature_plan.prenom)}.{slugify(candidature_plan.nom)}"
                f".{len(candidatures_creees)}{_EMAIL_DOMAIN}"
            )
            cv = _cv(rng, CORPUS[spec["intitule"]], candidature_plan, email)
            candidat: ProfilCandidatModel = CandidatDjangoFactory(  # type: ignore[assignment]
                utilisateur__first_name=candidature_plan.prenom,
                utilisateur__last_name=candidature_plan.nom,
                utilisateur__email=email,
                utilisateur__password=None,
                resume="\n".join(texte for texte, _ in cv.lignes),
            )
            candidature: CandidatureModel = CandidatureDjangoFactory(  # type: ignore[assignment]
                candidat=candidat,
                etape=etapes[candidature_plan.etape],
                statut=StatutCandidature.SOUMISE.value,
                motif_refus=next(motifs_refus)
                if candidature_plan.etape == _REFUS
                else None,
            )
            _seed_cv(candidature, candidat.utilisateur, _pdf_texte(cv.lignes))
            if candidature_plan.note:
                NoteDjangoFactory(
                    candidature=candidature,
                    publie_par=responsable,
                    message=_note(candidature_plan, spec["intitule"], cv),
                )
            if candidature_plan.conversation:
                _seed_conversation(
                    candidature,
                    candidature_plan,
                    responsable.utilisateur,
                    creneaux,
                    nb_conversations % len(creneaux),
                    envois,
                )
                nb_conversations += 1
            depose_au_plus_tard = fin
            if candidature_plan.conversation:
                depose_au_plus_tard = min(fin, envois[0] - timedelta(days=1))
            candidature.created_at = fake.date_time_between(
                fin - _CANDIDATURES_ETALEES_SUR,
                depose_au_plus_tard,
                tzinfo=fin.tzinfo,
            )
            candidatures_creees.append(candidature)
    CandidatureModel.objects.bulk_update(candidatures_creees, ["created_at"])


def seed_demo_organisme(
    organisme_id: UUID, force: bool = False, dry_run: bool = False
) -> dict:
    try:
        organisme, agents = _cible(organisme_id)
    except _SeedRefuse as refus:
        return refus.contexte

    factory.random.reseed_random(_SEED)
    fake = Faker("fr_FR")
    fake.seed_instance(_SEED)
    rng = random.Random(_SEED)
    plans = _planifier(fake, rng)

    if dry_run:
        return {
            "status": "dry_run",
            "comptes": _comptes(plans),
            "a_supprimer": _a_supprimer(),
        }
    if _offres_demo().exists() and not force:
        return {"status": "already_seeded"}

    with transaction.atomic():
        if force:
            _supprimer_demo()
        _ecrire(plans, organisme, agents, fake, rng)
    return {"status": "seeded", "comptes": _comptes(plans)}
