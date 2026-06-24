from datetime import UTC, datetime
from uuid import uuid4

from referentiel.value_objects.category import Category
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.recruteur.models import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.referentiel.metier_factory import MetierFactory
from tests.factories.referentiel.offer_factory import OfferFactory

# Sentinelle pour l'idempotence : si cet email existe, le seed a déjà tourné.
_SEED_SENTINEL_EMAIL = "marie.dupont@transition-eco.gouv.fr"

_ORGANISME_SIRET = "21050023700354"


def seed_recruteur_datas() -> dict:
    if UserModel.objects.filter(email=_SEED_SENTINEL_EMAIL).exists():
        return {"status": "already_seeded"}

    # ------------------------------------------------------------------ #
    # 1. Organisme recruteur                                               #
    # ------------------------------------------------------------------ #
    organisme, _ = OrganismeModel.objects.get_or_create(
        siret=_ORGANISME_SIRET,
        defaults={
            "id": uuid4(),
            "nom": "Ministère de la Transition Écologique",
            "versant": Verse.FPE.value,
        },
    )

    # ------------------------------------------------------------------ #
    # 2. Métiers                                                           #
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
    AgentFactory.create_model(
        prenom="Marie",
        nom="Dupont",
        email=_SEED_SENTINEL_EMAIL,
    )
    AgentFactory.create_model(
        prenom="Paul",
        nom="Bernard",
        email="paul.bernard@transition-eco.gouv.fr",
    )
    AgentFactory.create_model(
        prenom="Claire",
        nom="Moreau",
        email="claire.moreau@transition-eco.gouv.fr",
    )

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
    OfferFactory.create_model(
        title="Directeur des systèmes d'information",
        reference="REF-2024-A01",
        external_id="SEED-ARCHIVE-001",
        verse=Verse.FPE,
        category=Category.A,
        publication_date=datetime(2024, 12, 1, tzinfo=UTC),
        archived_at=datetime(2025, 3, 1),
    )
    OfferFactory.create_model(
        title="Chef de projet transformation numérique",
        reference="REF-2024-A02",
        external_id="SEED-ARCHIVE-002",
        verse=Verse.FPE,
        category=Category.A,
        publication_date=datetime(2024, 11, 15, tzinfo=UTC),
        archived_at=datetime(2025, 2, 15),
    )
    OfferFactory.create_model(
        title="Conseiller en mobilité professionnelle",
        reference="REF-2024-A03",
        external_id="SEED-ARCHIVE-003",
        verse=Verse.FPT,
        category=Category.B,
        publication_date=datetime(2024, 10, 1, tzinfo=UTC),
        archived_at=datetime(2025, 1, 15),
    )

    # ------------------------------------------------------------------ #
    # 6. Candidats (8)                                                     #
    # ------------------------------------------------------------------ #
    candidats = [
        CandidatFactory.create_model(
            prenom="Alice", nom="Martin", email="alice.martin@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Thomas", nom="Petit", email="thomas.petit@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Sophie", nom="Leblanc", email="sophie.leblanc@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Lucas", nom="Fontaine", email="lucas.fontaine@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Emma", nom="Rousseau", email="emma.rousseau@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Hugo", nom="Garnier", email="hugo.garnier@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Léa", nom="Chevalier", email="lea.chevalier@candidat.fr"
        ),
        CandidatFactory.create_model(
            prenom="Nathan", nom="Morel", email="nathan.morel@candidat.fr"
        ),
    ]

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

    return {
        "status": "seeded",
        "organisme_id": str(organisme.id),
        "nb_offres_actives": len(offres_actives),
        "nb_offres_archivees": 3,
        "nb_candidats": len(candidats),
        "nb_agents": 3,
    }
