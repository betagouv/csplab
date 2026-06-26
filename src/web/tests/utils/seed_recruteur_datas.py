from datetime import UTC, datetime
from uuid import UUID

from referentiel.value_objects.category import Category
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.identite.value_objects.siret import SIRET
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.identite.organisme_factory import OrganismeFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.factories.referentiel.metier_factory import MetierFactory
from tests.factories.referentiel.offer_factory import OfferFactory

# Sentinelle pour l'idempotence : si cet email existe, le seed a déjà tourné.
_SEED_SENTINEL_EMAIL = "marie.dupont@transition-eco.gouv.fr"

_ORGANISME_SIRET = "21050023700354"

_AGENTS_SPECS = [
    {"prenom": "Marie", "nom": "Dupont", "email": _SEED_SENTINEL_EMAIL},
    {
        "prenom": "Paul",
        "nom": "Bernard",
        "email": "paul.bernard@transition-eco.gouv.fr",
    },
    {
        "prenom": "Claire",
        "nom": "Moreau",
        "email": "claire.moreau@transition-eco.gouv.fr",
    },
]

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

_ALL_SEED_EMAILS = [s["email"] for s in _AGENTS_SPECS + _CANDIDATS_SPECS]

_SEED_OFFER_EXTERNAL_IDS = [
    "SEED-ACTIF-001",
    "SEED-ACTIF-002",
    "SEED-ACTIF-003",
    "SEED-ACTIF-004",
    "SEED-ACTIF-005",
    "SEED-ACTIF-006",
    "SEED-ARCHIVE-001",
    "SEED-ARCHIVE-002",
    "SEED-ARCHIVE-003",
]

_SEED_METIER_OFFER_FAMILY_CODES = ["ERNUM001", "ERJUR001"]


def _delete_seed_data() -> None:
    RecrutementModel.objects.filter(organisme__siret=_ORGANISME_SIRET).delete()  # type: ignore[attr-defined]

    seed_offer_ids = list(
        OfferModel.objects.filter(external_id__in=_SEED_OFFER_EXTERNAL_IDS).values_list(
            "id", flat=True
        )
    )
    CandidatureModel.objects.filter(offre_id__in=seed_offer_ids).delete()

    # ProfilAgentModel/ProfilCandidatModel utilisent to_field="username" :
    # utilisateur_id stocke le username (UUID entité), pas le PK id.
    seed_usernames = list(
        UserModel.objects.filter(email__in=_ALL_SEED_EMAILS).values_list(
            "username", flat=True
        )
    )
    ProfilAgentModel.objects.filter(utilisateur_id__in=seed_usernames).delete()
    ProfilCandidatModel.objects.filter(utilisateur_id__in=seed_usernames).delete()
    UserModel.objects.filter(email__in=_ALL_SEED_EMAILS).delete()

    OfferModel.objects.filter(external_id__in=_SEED_OFFER_EXTERNAL_IDS).delete()
    MetierModel.objects.filter(
        offer_family_code__in=_SEED_METIER_OFFER_FAMILY_CODES
    ).delete()
    OrganismeModel.objects.filter(siret=_ORGANISME_SIRET).delete()


def seed_recruteur_datas(force: bool = False) -> dict:
    if UserModel.objects.filter(email=_SEED_SENTINEL_EMAIL).exists():
        if not force:
            return {"status": "already_seeded"}
        _delete_seed_data()

    # ------------------------------------------------------------------ #
    # 1. Organisme recruteur                                             #
    # ------------------------------------------------------------------ #
    organisme = OrganismeFactory.create_model(
        nom="Ministère de la Transition Écologique",
        versant=Verse.FPE,
        siret=SIRET(_ORGANISME_SIRET),
    )

    # ------------------------------------------------------------------ #
    # 2. Métiers                                                         #
    # ------------------------------------------------------------------ #
    MetierFactory.create_model(
        libelle="Chargé de mission numérique",
        domaine_fonctionnel_code="NUM",
        offer_family_code="ERNUM001",
    )
    MetierFactory.create_model(
        libelle="Juriste droit public",
        domaine_fonctionnel_code="JUR",
        offer_family_code="ERJUR001",
    )

    # ------------------------------------------------------------------ #
    # 3. Agents / recruteurs                                               #
    # ------------------------------------------------------------------ #
    agents = [AgentFactory.create_model(**spec) for spec in _AGENTS_SPECS]
    agent_marie = agents[0]  # responsable par défaut (Marie Dupont)

    # ------------------------------------------------------------------ #
    # 4. Offres actives (6)                                                #
    # ------------------------------------------------------------------ #
    offres_actives = [
        OfferFactory.create_model(
            title="Chargé de mission numérique",
            reference="REF-2025-001",
            external_id="SEED-ACTIF-001",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2025, 6, 22, tzinfo=UTC),
        ),
        OfferFactory.create_model(
            title="Responsable RH",
            reference="REF-2025-002",
            external_id="SEED-ACTIF-002",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2025, 6, 22, tzinfo=UTC),
        ),
        OfferFactory.create_model(
            title="Ingénieur infrastructure cloud",
            reference="REF-2025-003",
            external_id="SEED-ACTIF-003",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2025, 6, 21, tzinfo=UTC),
        ),
        OfferFactory.create_model(
            title="Juriste droit public",
            reference="REF-2025-004",
            external_id="SEED-ACTIF-004",
            verse=Verse.FPT,
            category=Category.A,
            publication_date=datetime(2025, 6, 21, tzinfo=UTC),
        ),
        OfferFactory.create_model(
            title="Chargé de communication",
            reference="REF-2025-005",
            external_id="SEED-ACTIF-005",
            verse=Verse.FPE,
            category=Category.B,
            publication_date=datetime(2025, 6, 2, tzinfo=UTC),
        ),
        OfferFactory.create_model(
            title="Analyste budgétaire",
            reference="REF-2025-006",
            external_id="SEED-ACTIF-006",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2025, 6, 1, tzinfo=UTC),
        ),
    ]

    # ------------------------------------------------------------------ #
    # 5. Offres archivées (3)                                              #
    # ------------------------------------------------------------------ #
    offres_archivees = [
        OfferFactory.create_model(
            title="Directeur des systèmes d'information",
            reference="REF-2024-A01",
            external_id="SEED-ARCHIVE-001",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2024, 12, 1, tzinfo=UTC),
            archived_at=datetime(2025, 3, 1),
        ),
        OfferFactory.create_model(
            title="Chef de projet transformation numérique",
            reference="REF-2024-A02",
            external_id="SEED-ARCHIVE-002",
            verse=Verse.FPE,
            category=Category.A,
            publication_date=datetime(2024, 11, 15, tzinfo=UTC),
            archived_at=datetime(2025, 2, 15),
        ),
        OfferFactory.create_model(
            title="Conseiller en mobilité professionnelle",
            reference="REF-2024-A03",
            external_id="SEED-ARCHIVE-003",
            verse=Verse.FPT,
            category=Category.B,
            publication_date=datetime(2024, 10, 1, tzinfo=UTC),
            archived_at=datetime(2025, 1, 15),
        ),
    ]

    # ------------------------------------------------------------------ #
    # 6. Candidats (8)                                                     #
    # ------------------------------------------------------------------ #
    candidats = [CandidatFactory.create_model(**spec) for spec in _CANDIDATS_SPECS]

    # ------------------------------------------------------------------ #
    # 7. Candidatures                                                      #
    # ------------------------------------------------------------------ #
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

    for candidat_model, offre_model, statut in candidatures_specs:
        CandidatureFactory.build_model(
            candidat_id=candidat_model.to_entity().entity_id,
            offre_id=offre_model.id,
            statut=statut,
        )

    # ------------------------------------------------------------------ #
    # 8. Recrutements actifs (6)                                           #
    # ------------------------------------------------------------------ #
    agent_responsable_id = UUID(agent_marie.utilisateur_id)  # type: ignore[attr-defined]

    for offre in offres_actives:
        RecrutementFactory.create_model(
            offre_id=offre.id,
            organisme_id=organisme.id,
            responsables_ids=(agent_responsable_id,),
            status=RecrutementStatus.ACTIF,
        )

    # ------------------------------------------------------------------ #
    # 9. Recrutements archivés (3)                                         #
    # ------------------------------------------------------------------ #
    archives_specs = [
        (offres_archivees[0], UUID(candidats[0].utilisateur_id)),  # type: ignore[attr-defined]  # Alice → finalisé
        (offres_archivees[1], UUID(candidats[1].utilisateur_id)),  # type: ignore[attr-defined]  # Thomas → finalisé
        (offres_archivees[2], None),  # non finalisé
    ]

    for offre, candidat_id in archives_specs:
        RecrutementFactory.create_model(
            offre_id=offre.id,
            organisme_id=organisme.id,
            responsables_ids=(agent_responsable_id,),
            status=RecrutementStatus.ARCHIVE,
            candidat_recrute_id=candidat_id,
        )

    return {
        "status": "seeded",
        "organisme_id": str(organisme.id),
        "nb_offres_actives": len(offres_actives),
        "nb_offres_archivees": len(offres_archivees),
        "nb_recrutements_actifs": len(offres_actives),
        "nb_recrutements_archives": len(archives_specs),
        "nb_candidats": len(candidats),
        "nb_agents": len(agents),
    }
