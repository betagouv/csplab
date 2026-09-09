import os
import secrets
from datetime import UTC, datetime
from uuid import UUID

from django.db import transaction
from django.utils import timezone
from factory.django import Password
from referentiel.value_objects.category import Category
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementModel,
)
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

# Sentinelle pour l'idempotence : si cet email existe, le seed a déjà tourné.
_SEED_SENTINEL_EMAIL = "marie.dupont.gouv.fr@yopmail.com"

_ORGANISME_SIRET = "21050023700354"
_ORGANISME_UUID = UUID("00000000-0000-0000-0000-000000000000")

# Organismes supplémentaires : le second sert à éprouver la bascule d'organisme,
# le troisième reste sans recrutement pour éprouver l'état vide.
_BRIANCON_UUID = UUID("00000000-0000-0000-0000-000000000001")
_CHU_UUID = UUID("00000000-0000-0000-0000-000000000002")

_ORGANISMES_SECONDAIRES_SPECS = [
    {
        "entity_id": _BRIANCON_UUID,
        "nom": "Commune de Briançon",
        "versant": Verse.FPT,
        "siret": "21050056100019",
    },
    {
        "entity_id": _CHU_UUID,
        "nom": "CHU de Bordeaux",
        "versant": Verse.FPH,
        "siret": "26330001500017",
    },
]

_ALL_SEED_ORGANISME_UUIDS = [_ORGANISME_UUID] + [
    spec["entity_id"] for spec in _ORGANISMES_SECONDAIRES_SPECS
]
_ALL_SEED_ORGANISME_SIRETS = [_ORGANISME_SIRET] + [
    spec["siret"] for spec in _ORGANISMES_SECONDAIRES_SPECS
]

_AGENTS_SPECS = [
    {"prenom": "Marie", "nom": "Dupont", "email": _SEED_SENTINEL_EMAIL},
    {
        "prenom": "Paul",
        "nom": "Bernard",
        "email": "paul.bernard.gouv.fr@yopmail.com",
    },
    {
        "prenom": "Claire",
        "nom": "Moreau",
        "email": "claire.moreau.gouv.fr@yopmail.com",
    },
    {
        "prenom": "David",
        "nom": "Roux",
        "email": "david.roux.gouv.fr@yopmail.com",
    },
    {
        "prenom": "Marc",
        "nom": "Pelletier",
        "email": "marc.pelletier.gouv.fr@yopmail.com",
    },
]

_ADMIN_SPEC = {
    "prenom": "Isabelle",
    "nom": "Girard",
    "email": "isabelle.girard.gouv.fr@yopmail.com",
}

_CANDIDATS_SPECS = [
    {"prenom": "Alice", "nom": "Martin", "email": "alice.martin@candidat.fr"},
    {"prenom": "Thomas", "nom": "Petit", "email": "thomas.petit@candidat.fr"},
    {"prenom": "Sophie", "nom": "Leblanc", "email": "sophie.leblanc@candidat.fr"},
    {"prenom": "Lucas", "nom": "Fontaine", "email": "lucas.fontaine@candidat.fr"},
    {"prenom": "Emma", "nom": "Rousseau", "email": "emma.rousseau@candidat.fr"},
    {"prenom": "Hugo", "nom": "Garnier", "email": "hugo.garnier@candidat.fr"},
    {"prenom": "Léa", "nom": "Chevalier", "email": "lea.chevalier@candidat.fr"},
    {"prenom": "Nathan", "nom": "Morel", "email": "nathan.morel@candidat.fr"},
]

_ALL_SEED_EMAILS = [
    s["email"] for s in _AGENTS_SPECS + _CANDIDATS_SPECS + [_ADMIN_SPEC]
]

_SEED_OFFER_EXTERNAL_IDS = [
    "SEED-ACTIF-001",
    "SEED-ACTIF-002",
    "SEED-ACTIF-003",
    "SEED-ACTIF-004",
    "SEED-ACTIF-005",
    "SEED-ACTIF-006",
    "SEED-ACTIF-007",
    "SEED-B-ACTIF-001",
    "SEED-B-ACTIF-002",
    "SEED-ARCHIVE-001",
    "SEED-ARCHIVE-002",
    "SEED-ARCHIVE-003",
]

_SEED_METIER_OFFER_FAMILY_CODES = ["ERNUM001", "ERJUR001"]


def _delete_seed_data() -> None:
    seed_usernames = list(
        UserModel.objects.filter(email__in=_ALL_SEED_EMAILS).values_list(
            "username", flat=True
        )
    )
    CandidatureModel.objects.filter(candidat_id__in=seed_usernames).delete()

    seed_offre_ids = OfferModel.objects.filter(
        external_id__in=_SEED_OFFER_EXTERNAL_IDS
    ).values_list("id", flat=True)
    RecrutementModel.objects.filter(offre_id__in=seed_offre_ids).delete()  # type: ignore[attr-defined]

    OrganismeAgentModel.objects.filter(
        organisme_id__in=_ALL_SEED_ORGANISME_UUIDS
    ).delete()
    ProfilAgentModel.objects.filter(utilisateur_id__in=seed_usernames).delete()
    ProfilCandidatModel.objects.filter(utilisateur_id__in=seed_usernames).delete()
    UserModel.objects.filter(email__in=_ALL_SEED_EMAILS).delete()

    OfferModel.objects.filter(external_id__in=_SEED_OFFER_EXTERNAL_IDS).delete()
    MetierModel.objects.filter(
        offer_family_code__in=_SEED_METIER_OFFER_FAMILY_CODES
    ).delete()
    OrganismeModel.objects.filter(siret__in=_ALL_SEED_ORGANISME_SIRETS).delete()


def seed_recruteur_datas(force: bool = False) -> dict:
    if UserModel.objects.filter(email=_SEED_SENTINEL_EMAIL).exists():
        if not force:
            return {"status": "already_seeded"}
        _delete_seed_data()

    with transaction.atomic():
        # -------------------------------------------------------------- #
        # Organisme recruteur                                            #
        # -------------------------------------------------------------- #
        organisme = OrganismeDjangoFactory(
            id=_ORGANISME_UUID,
            nom="Ministère de la Transition Écologique",
            versant=Verse.FPE.value,
            siret=_ORGANISME_SIRET,
            gestion_ats=False,
            etapes=EtapeRecrutementFactory.create_entity_batch(),
        )

        organismes = {_ORGANISME_UUID: organisme}
        for spec in _ORGANISMES_SECONDAIRES_SPECS:
            organismes[spec["entity_id"]] = OrganismeDjangoFactory(
                id=spec["entity_id"],
                nom=spec["nom"],
                versant=spec["versant"].value,
                siret=spec["siret"],
                gestion_ats=False,
                etapes=EtapeRecrutementFactory.create_entity_batch(),
            )

        # -------------------------------------------------------------- #
        # Métiers                                                        #
        # -------------------------------------------------------------- #
        MetierDjangoFactory(
            libelle_long="Chargé de mission numérique",
            domaine_fonctionnel_code="NUM",
            offer_family_code="ERNUM001",
        )
        MetierDjangoFactory(
            libelle_long="Juriste droit public",
            domaine_fonctionnel_code="JUR",
            offer_family_code="ERJUR001",
        )

        # -------------------------------------------------------------- #
        # Agents / recruteurs                                            #
        # -------------------------------------------------------------- #
        # Mot de passe généré à chaque seed (visible dans les logs de déploiement)
        seed_password = os.environ.get("SEED_USER_PASSWORD") or secrets.token_urlsafe(
            16
        )
        agents = {
            spec["prenom"]: AgentDjangoFactory(
                utilisateur__first_name=spec["prenom"],
                utilisateur__last_name=spec["nom"],
                utilisateur__email=spec["email"],
                utilisateur__password=Password(seed_password),
            )
            for spec in _AGENTS_SPECS
        }

        # Marie est responsable du premier organisme, Paul et Claire en sont membres.
        # Marc est membre du premier et responsable du second : c'est lui qui permet
        # d'éprouver la bascule d'organisme et l'apparition des pages de paramètres.
        # David ne l'est d'aucun, pour éprouver la navigation vide et le refus d'accès.
        _ATTACHEMENTS = [
            (_ORGANISME_UUID, "Marie", AgentOrganismeRole.RESPONSABLE),
            (_ORGANISME_UUID, "Paul", AgentOrganismeRole.MEMBRE),
            (_ORGANISME_UUID, "Claire", AgentOrganismeRole.MEMBRE),
            (_ORGANISME_UUID, "Marc", AgentOrganismeRole.MEMBRE),
            (_BRIANCON_UUID, "Marc", AgentOrganismeRole.RESPONSABLE),
        ]
        for organisme_uuid, agent_prenom, role in _ATTACHEMENTS:
            OrganismeAgentDjangoFactory(
                organisme=organismes[organisme_uuid],
                agent=agents[agent_prenom],
                role=role.value,
            )

        # -------------------------------------------------------------- #
        # Administrateur (staff, hors organisme)                         #
        # -------------------------------------------------------------- #
        admin = UtilisateurDjangoFactory(
            password=Password(seed_password),
            is_staff=True,
            first_name=_ADMIN_SPEC["prenom"],
            last_name=_ADMIN_SPEC["nom"],
            email=_ADMIN_SPEC["email"],
        )

        # -------------------------------------------------------------- #
        # Offres actives (6)                                             #
        # -------------------------------------------------------------- #
        offres_actives = [
            OfferDjangoFactory(
                title="Chargé de mission numérique",
                reference="REF-2025-001",
                external_id="SEED-ACTIF-001",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 22, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Responsable RH",
                reference="REF-2025-002",
                external_id="SEED-ACTIF-002",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 22, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Ingénieur infrastructure cloud",
                reference="REF-2025-003",
                external_id="SEED-ACTIF-003",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 21, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Juriste droit public",
                reference="REF-2025-004",
                external_id="SEED-ACTIF-004",
                verse=Verse.FPT.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 21, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Chargé de communication",
                reference="REF-2025-005",
                external_id="SEED-ACTIF-005",
                verse=Verse.FPE.value,
                category=Category.B.value,
                publication_date=datetime(2025, 6, 2, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Analyste budgétaire",
                reference="REF-2025-006",
                external_id="SEED-ACTIF-006",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 1, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Chargé de mission",
                reference="REF-2025-006",
                external_id="SEED-ACTIF-007",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2025, 6, 1, tzinfo=UTC),
            ),
        ]

        # -------------------------------------------------------------- #
        # Offres archivées (3)                                           #
        # -------------------------------------------------------------- #
        offres_archivees = [
            OfferDjangoFactory(
                title="Directeur des systèmes d'information",
                reference="REF-2024-A01",
                external_id="SEED-ARCHIVE-001",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2024, 12, 1, tzinfo=UTC),
                archived_at=timezone.make_aware(datetime(2025, 3, 1)),
            ),
            OfferDjangoFactory(
                title="Chef de projet transformation numérique",
                reference="REF-2024-A02",
                external_id="SEED-ARCHIVE-002",
                verse=Verse.FPE.value,
                category=Category.A.value,
                publication_date=datetime(2024, 11, 15, tzinfo=UTC),
                archived_at=timezone.make_aware(datetime(2025, 2, 15)),
            ),
            OfferDjangoFactory(
                title="Conseiller en mobilité professionnelle",
                reference="REF-2024-A03",
                external_id="SEED-ARCHIVE-003",
                verse=Verse.FPT.value,
                category=Category.B.value,
                publication_date=datetime(2024, 10, 1, tzinfo=UTC),
                archived_at=timezone.make_aware(datetime(2025, 1, 15)),
            ),
        ]

        # -------------------------------------------------------------- #
        # Offres du second organisme                                     #
        # -------------------------------------------------------------- #
        offres_briancon = [
            OfferDjangoFactory(
                title="Agent technique polyvalent",
                reference="REF-2025-B01",
                external_id="SEED-B-ACTIF-001",
                verse=Verse.FPT.value,
                category=Category.C.value,
                publication_date=datetime(2025, 5, 12, tzinfo=UTC),
            ),
            OfferDjangoFactory(
                title="Responsable des services techniques",
                reference="REF-2025-B02",
                external_id="SEED-B-ACTIF-002",
                verse=Verse.FPT.value,
                category=Category.B.value,
                publication_date=datetime(2025, 5, 20, tzinfo=UTC),
            ),
        ]

        # -------------------------------------------------------------- #
        # Candidats (8)                                                  #
        # -------------------------------------------------------------- #
        candidats = [
            CandidatDjangoFactory(
                utilisateur__first_name=spec["prenom"],
                utilisateur__last_name=spec["nom"],
                utilisateur__email=spec["email"],
                utilisateur__password=Password(seed_password),
            )
            for spec in _CANDIDATS_SPECS
        ]

        # -------------------------------------------------------------- #
        # Recrutements (1 / offre active et archivée): étapes + responsables
        # -------------------------------------------------------------- #
        marie = agents["Marie"]
        paul = agents["Paul"]
        claire = agents["Claire"]
        marc = agents["Marc"]

        recrutements_specs = [
            (
                _ORGANISME_UUID,
                offres_actives[0],
                marie,
                (paul, AgentRecrutementRole.RECRUTEUR),
            ),
            (
                _ORGANISME_UUID,
                offres_actives[1],
                marie,
                (paul, AgentRecrutementRole.RECRUTEUR),
            ),
            (
                _ORGANISME_UUID,
                offres_actives[2],
                marie,
                (paul, AgentRecrutementRole.RECRUTEUR),
            ),
            (
                _ORGANISME_UUID,
                offres_actives[3],
                claire,
                (paul, AgentRecrutementRole.CONTRIBUTEUR),
            ),
            (_ORGANISME_UUID, offres_actives[4], claire, None),
            (_ORGANISME_UUID, offres_actives[5], claire, None),
            (
                _ORGANISME_UUID,
                offres_actives[6],
                marie,
                (paul, AgentRecrutementRole.RECRUTEUR),
            ),
            (_ORGANISME_UUID, offres_archivees[0], claire, None),
            (_ORGANISME_UUID, offres_archivees[1], claire, None),
            (_ORGANISME_UUID, offres_archivees[2], claire, None),
            (_BRIANCON_UUID, offres_briancon[0], marc, None),
            (_BRIANCON_UUID, offres_briancon[1], marc, None),
        ]

        recrutements = []
        for organisme_uuid, offre, responsable, extra_agent in recrutements_specs:
            recrutement = RecrutementDjangoFactory(
                offre=offre,
                organisme=organismes[organisme_uuid],
                agent_link__agent=responsable,
                agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
            )
            if extra_agent is not None:
                extra_agent_model, extra_agent_role = extra_agent
                RecrutementAgentDjangoFactory(
                    recrutement=recrutement,
                    agent=extra_agent_model,
                    role=extra_agent_role.value,
                )
            recrutements.append(recrutement)

        # -------------------------------------------------------------- #
        # Candidatures                                                   #
        # -------------------------------------------------------------- #
        candidatures_specs = [
            (candidats[0], offres_actives[0], StatutCandidature.SOUMISE),
            (candidats[1], offres_actives[0], StatutCandidature.INITIAL),
            (candidats[2], offres_actives[0], StatutCandidature.SOUMISE),
            (candidats[0], offres_actives[1], StatutCandidature.SOUMISE),
            (candidats[3], offres_actives[1], StatutCandidature.INITIAL),
            (candidats[4], offres_actives[2], StatutCandidature.SOUMISE),
            (candidats[5], offres_actives[3], StatutCandidature.SOUMISE),
            (candidats[6], offres_actives[3], StatutCandidature.INITIAL),
            (candidats[1], offres_actives[4], StatutCandidature.SOUMISE),
            (candidats[7], offres_actives[5], StatutCandidature.INITIAL),
        ]

        recrutements_by_offre_id = {
            r.pk: r  # type: ignore[attr-defined]
            for r in recrutements
        }
        for candidat_model, offre_model, statut in candidatures_specs:
            recrutement = recrutements_by_offre_id[offre_model.id]
            etape = recrutement.etapes.get(  # type: ignore[attr-defined]
                categorie=CategorieEtapeRecrutement.ENTREE.value
            )
            CandidatureDjangoFactory(
                candidat=candidat_model,
                etape=etape,
                statut=statut.value,
            )

        return {
            "status": "seeded",
            "organisme_id": str(organisme.id),
            "nb_offres_actives": len(offres_actives),
            "nb_offres_archivees": len(offres_archivees),
            "nb_candidats": len(candidats),
            "nb_agents": len(agents),
            "nb_recrutements": len(recrutements),
            "seed_password": seed_password,
            "admin_email": admin.email,
        }
