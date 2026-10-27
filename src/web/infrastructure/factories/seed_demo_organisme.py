import os
import random
import textwrap
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from itertools import cycle
from uuid import UUID

import factory.random
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.text import slugify
from faker import Faker
from referentiel.value_objects.source_type import SourceType

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.note import NoteModel
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
    NOTE_CONCLUSIONS_APPEL,
    NOTE_DISPONIBILITES,
    NOTE_FORMATS,
    NOTE_MOTIVATIONS,
    NOTE_PRESENTS,
    NOTE_QUALITES,
    NOTE_SUITES,
    NOTE_VIGILANCES,
    VILLES,
    Experience,
    Formation,
    PosteCorpus,
)
from infrastructure.factories.seed_demo_specs import RecrutementSpec, SpecOrganisme
from infrastructure.factories.seed_recruteur_datas import delete_candidatures

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

_PREMIER_APPEL = "Premier appel"
_COMPTE_RENDU = "Compte rendu d'entretien"
_NOTES_PAR_ETAPE = {
    _PRESELECTION: (_PREMIER_APPEL,),
    _ENTRETIEN: (_COMPTE_RENDU,),
    _RECRUTEMENT: (_PREMIER_APPEL, _COMPTE_RENDU),
}
_GRADES = ("A", "B", "C")
_DUREES_ENTRETIEN = (30, 45, 60)
_SUITE_SECOND_ENTRETIEN = "Proposer un créneau pour un second entretien"

_SAMEDI = 5
_CRENEAUX = ((3, "10 h"), (5, "14 h 30"), (8, "11 h"))
_CANDIDATURES_ETALEES_SUR = timedelta(days=30)
_DEMANDE_ENVOYEE_A = time(9, 30)
_REPONSE_ENVOYEE_A = time(16, 30)
_AVIS = {
    0.4: (
        "Réservé. Parcours voisin du poste, adéquation à confirmer.",
        "Réservé. Expériences utiles mais éloignées des missions principales.",
    ),
    0.65: (
        "Favorable avec réserves. Profil en partie aligné, à accompagner.",
        "Favorable avec réserves. Bonnes bases, missions du poste à découvrir.",
    ),
    0.9: (
        "Favorable. Profil solide, à revoir en second entretien avec la direction.",
        "Favorable. Parcours en adéquation directe avec les missions du poste.",
    ),
}
_PROXIMITE_RETENUE = 0.9
_PART_AVATAR = 0.5
_COULEURS_AVATAR = (
    (0.0, 0.0, 0.57),
    (0.88, 0.0, 0.06),
    (0.0, 0.45, 0.4),
    (0.42, 0.25, 0.6),
)


@dataclass
class _Avatar:
    initiales: str
    couleur: tuple[float, float, float]


@dataclass
class _CandidaturePlan:
    etape: str
    prenom: str
    nom: str
    proximite: float
    notes: tuple[str, ...]
    conversation: bool
    lecture: bool
    avatar: _Avatar | None


@dataclass
class _RecrutementPlan:
    reference: str
    spec: RecrutementSpec
    corpus: PosteCorpus
    candidatures: list[_CandidaturePlan]


@dataclass
class _Cv:
    lignes: list[tuple[str, bool]]
    experiences: list[tuple[int, Experience]]
    formation: Formation
    competences_poste: list[str]


def _reference(cle: str, rang: int) -> str:
    return f"DEMO-{cle}-{rang:02d}"


def _planifier(
    spec_organisme: SpecOrganisme, fake: Faker, rng: random.Random
) -> list[_RecrutementPlan]:
    plans = []
    nb_conversations = 0
    for rang, spec in enumerate(spec_organisme.recrutements, start=1):
        candidatures = []
        for etape, nombre in zip(_ETAPES, spec["repartition"], strict=True):
            for rang_dans_l_etape in range(nombre):
                notes = _NOTES_PAR_ETAPE.get(etape, ())
                if etape != _RECRUTEMENT and rang_dans_l_etape % 2:
                    notes = ()
                proximite = rng.choice(list(_AVIS))
                if etape == _RECRUTEMENT:
                    proximite = _PROXIMITE_RETENUE
                conversation = (
                    etape == _ENTRETIEN and spec["archive_depuis_jours"] is None
                )
                lecture = False
                if conversation:
                    lecture = nb_conversations % 2 == 0
                    nb_conversations += 1
                prenom, nom = fake.first_name(), fake.last_name()
                avatar = None
                if rng.random() < _PART_AVATAR:
                    avatar = _Avatar(
                        initiales=f"{prenom[0]}{nom[0]}".upper(),
                        couleur=rng.choice(_COULEURS_AVATAR),
                    )
                candidatures.append(
                    _CandidaturePlan(
                        etape=etape,
                        prenom=prenom,
                        nom=nom,
                        proximite=proximite,
                        notes=notes,
                        conversation=conversation,
                        lecture=lecture,
                        avatar=avatar,
                    )
                )
        plans.append(
            _RecrutementPlan(
                reference=_reference(spec_organisme.cle, rang),
                spec=spec,
                corpus=CORPUS[spec["famille"]],
                candidatures=candidatures,
            )
        )
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
        "notes": sum(len(c.notes) for c in candidatures),
        "conversations": sum(c.conversation for c in candidatures),
        "conversations_lues": sum(c.lecture for c in candidatures),
    }


def _offres_demo(organisme: OrganismeModel):
    return OfferModel.objects.filter(
        source_id=_SOURCE_DEMO_UUID, recrutement__organisme_id=organisme.pk
    )


def _candidatures_demo(organisme: OrganismeModel):
    return CandidatureModel.objects.filter(
        etape__recrutement__offre__in=_offres_demo(organisme)
    )


def _candidats_demo(organisme: OrganismeModel):
    return UserModel.objects.filter(
        email__endswith=_EMAIL_DOMAIN,
        profil_candidat__candidatures__in=_candidatures_demo(organisme),
    )


def _a_supprimer(organisme: OrganismeModel) -> dict:
    return {
        "offres": _offres_demo(organisme).count(),
        "candidatures": _candidatures_demo(organisme).count(),
        "candidats": _candidats_demo(organisme).count(),
    }


def _supprimer_demo(organisme: OrganismeModel) -> None:
    offres = list(_offres_demo(organisme).values_list("pk", flat=True))
    candidats = list(_candidats_demo(organisme).values_list("username", flat=True))
    delete_candidatures(
        list(_candidatures_demo(organisme).values_list("id", flat=True))
    )
    RecrutementModel.objects.filter(offre__in=offres).delete()
    OfferModel.objects.filter(pk__in=offres).delete()
    ProfilCandidatModel.objects.filter(utilisateur_id__in=candidats).delete()
    UserModel.objects.filter(username__in=candidats).delete()


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
_RAYON_AVATAR = 28
_KAPPA_CERCLE = 0.5523
_LIGNES_AVATAR = 6


def _flux_avatar(avatar: _Avatar) -> bytes:
    r, k = _RAYON_AVATAR, _RAYON_AVATAR * _KAPPA_CERCLE
    x, y = _MARGE + r, _PAGE[1] - _MARGE - r
    courbes = [
        (x + r, y + k, x + k, y + r, x, y + r),
        (x - k, y + r, x - r, y + k, x - r, y),
        (x - r, y - k, x - k, y - r, x, y - r),
        (x + k, y - r, x + r, y - k, x + r, y),
    ]
    return b"\n".join(
        [
            b"q",
            b"%.2f %.2f %.2f rg" % avatar.couleur,
            b"%.1f %.1f m" % (x + r, y),
            *(b"%.1f %.1f %.1f %.1f %.1f %.1f c" % courbe for courbe in courbes),
            b"f",
            b"BT /F2 18 Tf 1 1 1 rg %.1f %.1f Td (%s) Tj ET"
            % (x - 12, y - 6, _echapper(avatar.initiales)),
            b"Q",
        ]
    )


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


def _pdf_texte(lignes: list[tuple[str, bool]], avatar: _Avatar | None) -> bytes:
    coupees = [
        (morceau, gras)
        for texte, gras in lignes
        for morceau in textwrap.wrap(texte, width=_CARACTERES_PAR_LIGNE) or [""]
    ]
    if avatar is not None:
        coupees = [("", False)] * _LIGNES_AVATAR + coupees
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
        if avatar is not None and page_id == pages_ids[0]:
            flux = _flux_avatar(avatar) + b"\n" + flux
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
    rng.shuffle(experiences)
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
    durees = []
    for experience in experiences:
        duree = rng.randint(2, 4)
        durees.append(duree)
        debut = fin - duree
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
    formations = rng.sample(corpus["formations"], 2)
    for formation in formations:
        lignes.append(
            (f"{annee} : {formation['diplome']}, {formation['etablissement']}", False)
        )
        annee -= rng.randint(2, 3)
    lignes += [("", False), ("Compétences", True)]
    lignes += [(f"- {competence}", False) for competence in competences]
    lignes += [("", False), ("Langues", True), (rng.choice(LANGUES), False)]
    return _Cv(
        lignes=lignes,
        experiences=list(zip(durees, experiences, strict=True)),
        formation=formations[0],
        competences_poste=competences[:nb_competences_poste],
    )


def _jour(instant: datetime) -> str:
    return timezone.localtime(instant).strftime("%d/%m/%Y")


def _note_premier_appel(rng: random.Random, appel_le: datetime) -> str:
    fonctionnaire = rng.choice(("Oui", "Non"))
    grade = "sans objet, contractuel(le)"
    if fonctionnaire == "Oui":
        grade = rng.choice(_GRADES)
    return "\n".join(
        [
            _PREMIER_APPEL,
            f"Date de l'appel : {_jour(appel_le)}",
            f"Fonctionnaire : {fonctionnaire}",
            f"Grade : {grade}",
            f"Disponibilité : {rng.choice(NOTE_DISPONIBILITES)}",
            rng.choice(NOTE_CONCLUSIONS_APPEL),
        ]
    )


def _note_compte_rendu(
    rng: random.Random,
    corpus: PosteCorpus,
    candidature: _CandidaturePlan,
    cv: _Cv,
    entretien_le: datetime,
) -> str:
    parcours = [
        f"- {duree} ans comme {experience['titre']}, {experience['employeur']}"
        for duree, experience in cv.experiences[:2]
    ]
    a_approfondir = rng.choice(
        [c for c in corpus["competences_poste"] if c not in cv.competences_poste]
    )
    duree = rng.choice(_DUREES_ENTRETIEN)
    format_entretien = rng.choice(NOTE_FORMATS)
    suites = rng.sample(NOTE_SUITES, 2)
    if candidature.conversation:
        suites[0] = _SUITE_SECOND_ENTRETIEN
    return "\n".join(
        [
            _COMPTE_RENDU,
            f"Entretien du {_jour(entretien_le)} – {duree} min, {format_entretien}",
            f"Présents : {rng.choice(NOTE_PRESENTS)}",
            "",
            "Parcours",
            *parcours,
            f"- {cv.formation['diplome']}, {cv.formation['etablissement']}",
            "",
            "Motivations",
            *(f"- {motivation}" for motivation in rng.sample(NOTE_MOTIVATIONS, 2)),
            "",
            "Points forts",
            *(f"- {competence}" for competence in rng.sample(cv.competences_poste, 2)),
            f"- {rng.choice(NOTE_QUALITES)}",
            "",
            "Points de vigilance",
            f"- {a_approfondir} à approfondir",
            f"- {rng.choice(NOTE_VIGILANCES)}",
            "",
            "Avis",
            rng.choice(_AVIS[candidature.proximite]),
            "",
            "Suite",
            *(f"- {suite}" for suite in suites),
        ]
    )


def _instant_entre(rng: random.Random, debut: datetime, fin: datetime) -> datetime:
    return debut + (fin - debut) * rng.random()


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
    plan: _RecrutementPlan,
    organisme: OrganismeModel,
    source: SourceModel,
    responsable: ProfilAgentModel,
    maintenant: datetime,
) -> RecrutementModel:
    spec = plan.spec
    corpus = plan.corpus
    offre = {
        "source": source,
        "reference": plan.reference,
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


def _cible(
    organisme_id: UUID, spec_organisme: SpecOrganisme
) -> tuple[OrganismeModel, list[ProfilAgentModel]]:
    cle = spec_organisme.cle
    organisme = OrganismeModel.objects.by_id(organisme_id).first()
    if organisme is None:
        raise _SeedRefuse("organisme_absent", cle=cle, organisme_id=organisme_id)
    agents = [
        liaison.agent
        for liaison in OrganismeAgentModel.objects.active()
        .filter(organisme_id=organisme.pk)
        .select_related("agent__utilisateur")
        .order_by("created_at")
    ]
    if not agents:
        raise _SeedRefuse("aucun_agent_actif", cle=cle, organisme_id=organisme_id)
    autre_organisme_id = (
        RecrutementModel.objects.filter(
            offre__source_id=_SOURCE_DEMO_UUID,
            offre__reference__in=[
                _reference(cle, rang)
                for rang in range(1, len(spec_organisme.recrutements) + 1)
            ],
        )
        .exclude(organisme_id=organisme.pk)
        .values_list("organisme_id", flat=True)
        .first()
    )
    if autre_organisme_id is not None:
        raise _SeedRefuse(
            "cle_seedee_ailleurs",
            cle=cle,
            organisme_id=organisme_id,
            autre_organisme_id=autre_organisme_id,
        )
    return organisme, agents


def _ecrire(
    cle: str,
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
    notes_creees: list[NoteModel] = []
    nb_conversations = 0

    source, _ = SourceModel.objects.get_or_create(
        source_id=_SOURCE_DEMO_UUID,
        defaults={"slug": _SOURCE_DEMO_SLUG, "type": SourceType.API.value},
    )
    for plan in plans:
        spec = plan.spec
        responsable = next(responsables)
        autre_agent = next(
            (agent for agent in agents if agent.pk != responsable.pk), responsable
        )
        recrutement = _seed_recrutement(
            plan, organisme, source, responsable, maintenant
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
                f".{cle}-{len(candidatures_creees)}{_EMAIL_DOMAIN}"
            )
            cv = _cv(rng, plan.corpus, candidature_plan, email)
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
            _seed_cv(
                candidature,
                candidat.utilisateur,
                _pdf_texte(cv.lignes, candidature_plan.avatar),
            )
            depose_au_plus_tard = fin
            notes_au_plus_tard = fin
            if candidature_plan.conversation:
                depose_au_plus_tard = min(fin, envois[0] - timedelta(days=1))
                notes_au_plus_tard = envois[0]
            candidature.created_at = fake.date_time_between(
                fin - _CANDIDATURES_ETALEES_SUR,
                depose_au_plus_tard,
                tzinfo=fin.tzinfo,
            )
            candidatures_creees.append(candidature)
            publiee_le = candidature.created_at
            for nature in candidature_plan.notes:
                publiee_le = _instant_entre(rng, publiee_le, notes_au_plus_tard)
                auteur = responsable
                if nature == _PREMIER_APPEL:
                    message = _note_premier_appel(rng, publiee_le)
                    if candidature_plan.etape == _RECRUTEMENT:
                        auteur = autre_agent
                else:
                    message = _note_compte_rendu(
                        rng, plan.corpus, candidature_plan, cv, publiee_le
                    )
                note: NoteModel = NoteDjangoFactory(  # type: ignore[assignment]
                    candidature=candidature, publie_par=auteur, message=message
                )
                note.created_at = publiee_le
                notes_creees.append(note)
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
    CandidatureModel.objects.bulk_update(candidatures_creees, ["created_at"])
    NoteModel.objects.bulk_update(notes_creees, ["created_at"])


def _seed_un_organisme(
    spec_organisme: SpecOrganisme,
    organisme: OrganismeModel,
    agents: list[ProfilAgentModel],
    force: bool,
    dry_run: bool,
) -> dict:
    factory.random.reseed_random(spec_organisme.graine)
    fake = Faker("fr_FR")
    fake.seed_instance(spec_organisme.graine)
    rng = random.Random(spec_organisme.graine)
    plans = _planifier(spec_organisme, fake, rng)
    resultat = {"cle": spec_organisme.cle, "organisme_id": organisme.pk}

    if dry_run:
        return {
            **resultat,
            "status": "dry_run",
            "comptes": _comptes(plans),
            "a_supprimer": _a_supprimer(organisme),
        }
    if _offres_demo(organisme).exists() and not force:
        return {**resultat, "status": "already_seeded"}

    with transaction.atomic():
        if force:
            _supprimer_demo(organisme)
        _ecrire(spec_organisme.cle, plans, organisme, agents, fake, rng)
    return {**resultat, "status": "seeded", "comptes": _comptes(plans)}


def seed_demo_organisme(
    cibles: list[tuple[UUID, SpecOrganisme]],
    force: bool = False,
    dry_run: bool = False,
) -> dict:
    if os.environ.get("SCALEWAY_ENV") == "prod":
        return {"status": "production"}
    cles = {spec_organisme.cle for _, spec_organisme in cibles}
    organismes_ids = {organisme_id for organisme_id, _ in cibles}
    if len(cles) < len(cibles) or len(organismes_ids) < len(cibles):
        return {"status": "cible_en_double"}
    try:
        ciblees = [
            (spec_organisme, *_cible(organisme_id, spec_organisme))
            for organisme_id, spec_organisme in cibles
        ]
    except _SeedRefuse as refus:
        return refus.contexte
    return {
        "status": "ok",
        "organismes": [
            _seed_un_organisme(spec_organisme, organisme, agents, force, dry_run)
            for spec_organisme, organisme, agents in ciblees
        ],
    }
