import os
import secrets
from datetime import UTC, datetime
from uuid import UUID, uuid4

from referentiel.value_objects.category import Category
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.statut_candidature import StatutCandidature
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
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from infrastructure.factories.candidate.candidature_factory import CandidatureFactory
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.candidat_factory import CandidatFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
from infrastructure.factories.referentiel.metier_factory import MetierFactory
from infrastructure.factories.referentiel.offer_factory import OfferFactory

# Sentinelle pour l'idempotence : si cet email existe, le seed a déjà tourné.
_SEED_SENTINEL_EMAIL = "marie.dupont.gouv.fr@yopmail.com"

_ORGANISME_SIRET = "21050023700354"
_ORGANISME_UUID = UUID("00000000-0000-0000-0000-000000000000")

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

    seed_usernames = list(
        UserModel.objects.filter(email__in=_ALL_SEED_EMAILS).values_list(
            "username", flat=True
        )
    )
    OrganismeAgentModel.objects.filter(organisme_id=_ORGANISME_UUID).delete()
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
        entity_id=_ORGANISME_UUID,
        nom="Ministère de la Transition Écologique",
        versant=Verse.FPE,
        siret=SIRET(code=_ORGANISME_SIRET),
    )
    default_etapes_entities = EtapeRecrutementFactory.create_entity_batch()

    OrganismeModel.objects.filter(id=_ORGANISME_UUID).update(
        etapes=[
            {
                "entity_id": str(e.entity_id),
                "categorie": e.categorie.value,
                "nom": e.nom,
            }
            for e in default_etapes_entities
        ]
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
    # Mot de passe généré à chaque seed (visible dans les logs de déploiement)
    seed_password = os.environ.get("SEED_USER_PASSWORD") or secrets.token_urlsafe(16)
    agents = [
        AgentFactory.create_model(password=seed_password, username=None, **spec)
        for spec in _AGENTS_SPECS
    ]

    # Marie (agents[0]) est responsable de l'organisme, Paul et Claire en sont
    # membres ; David (agents[3]) reste hors de l'organisme pour tester le refus.
    OrganismeAgentModel(
        id=uuid4(),
        organisme_id=_ORGANISME_UUID,
        agent_id=agents[0].utilisateur_id,
        role=AgentOrganismeRole.RESPONSABLE.value,
    ).save()
    for agent in agents[1:3]:
        OrganismeAgentModel(
            id=uuid4(),
            organisme_id=_ORGANISME_UUID,
            agent_id=agent.utilisateur_id,
            role=AgentOrganismeRole.MEMBRE.value,
        ).save()

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
    candidats = [
        CandidatFactory.create_model(password=seed_password, username=None, **spec)
        for spec in _CANDIDATS_SPECS
    ]

    # ------------------------------------------------------------------ #
    # 7. Recrutements (1 par offre active et archivée) : étapes + responsables #
    # ------------------------------------------------------------------ #
    marie_id = agents[0].utilisateur_id
    paul_id = agents[1].utilisateur_id
    claire_id = agents[2].utilisateur_id
    david_id = agents[3].utilisateur_id

    recrutements_specs: list[
        tuple[OfferModel, UUID, tuple[UUID, AgentRecrutementRole] | None]
    ] = [
        (offres_actives[0], marie_id, (paul_id, AgentRecrutementRole.RECRUTEUR)),
        (offres_actives[1], marie_id, (paul_id, AgentRecrutementRole.RECRUTEUR)),
        (offres_actives[2], marie_id, (paul_id, AgentRecrutementRole.RECRUTEUR)),
        (offres_actives[3], claire_id, (david_id, AgentRecrutementRole.CONTRIBUTEUR)),
        (offres_actives[4], claire_id, None),
        (offres_actives[5], claire_id, None),
        (offres_archivees[0], claire_id, None),
        (offres_archivees[1], claire_id, None),
        (offres_archivees[2], claire_id, None),
    ]

    recrutements = []
    for offre, responsable_id, extra_agent in recrutements_specs:
        recrutement = RecrutementFactory.create_model(
            offre_id=offre.id,
            organisme_id=_ORGANISME_UUID,
            agent_id=responsable_id,
            agent_role=AgentRecrutementRole.RESPONSABLE,
        )
        if extra_agent is not None:
            extra_agent_id, extra_agent_role = extra_agent
            RecrutementAgentModel(
                id=uuid4(),
                recrutement=recrutement,
                agent_id=extra_agent_id,
                role=extra_agent_role.value,
            ).save()
        recrutements.append(recrutement)

    # ------------------------------------------------------------------ #
    # 8. Candidatures                                                      #
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
        CandidatureFactory.create_model(
            candidat_id=candidat_model.to_entity().entity_id,
            offre_id=offre_model.id,
            statut=statut,
        )

    return {
        "status": "seeded",
        "organisme_id": str(organisme.id),
        "nb_offres_actives": len(offres_actives),
        "nb_offres_archivees": 3,
        "nb_candidats": len(candidats),
        "nb_agents": len(agents),
        "nb_recrutements": len(recrutements),
        "seed_password": seed_password,
    }
