from dataclasses import dataclass
from typing import TypedDict

from infrastructure.factories.seed_demo_cv_corpus import Famille


class RecrutementSpec(TypedDict):
    intitule: str
    famille: Famille
    archive_depuis_jours: int | None
    repartition: tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class SpecOrganisme:
    cle: str
    graine: int
    recrutements: list[RecrutementSpec]


# repartition : candidatures par étape, dans l'ordre des étapes du recrutement.
_VOLUMES: list[tuple[int | None, tuple[int, int, int, int, int, int]]] = [
    (None, (0, 0, 0, 0, 0, 0)),
    (None, (2, 1, 1, 0, 1, 0)),
    (None, (2, 1, 1, 0, 1, 0)),
    (None, (2, 1, 1, 0, 1, 0)),
    (None, (16, 6, 3, 1, 4, 0)),
    (None, (22, 8, 4, 2, 6, 0)),
    (None, (26, 10, 5, 2, 8, 0)),
    (None, (31, 11, 6, 3, 9, 0)),
    (None, (94, 34, 18, 8, 46, 0)),
    (None, (90, 36, 20, 10, 44, 0)),
    (20, (0, 0, 0, 0, 19, 1)),
    (45, (0, 0, 0, 0, 20, 1)),
    (90, (0, 0, 0, 0, 21, 1)),
    (30, (3, 2, 1, 1, 4, 0)),
    (60, (5, 1, 2, 0, 3, 0)),
]


def _organisme(
    cle: str, graine: int, postes: list[tuple[str, Famille]]
) -> SpecOrganisme:
    return SpecOrganisme(
        cle=cle,
        graine=graine,
        recrutements=[
            {
                "intitule": intitule,
                "famille": famille,
                "archive_depuis_jours": archive_depuis_jours,
                "repartition": repartition,
            }
            for (intitule, famille), (archive_depuis_jours, repartition) in zip(
                postes, _VOLUMES, strict=True
            )
        ],
    )


_TRANSITION_ECOLOGIQUE = _organisme(
    "transition-ecologique",
    1946,
    [
        ("Inspecteur(trice) des installations classées", "environnement"),
        ("Chargé(e) d'instruction police de l'eau", "environnement"),
        ("Chargé(e) de mission risques naturels", "environnement"),
        (
            "Chargé(e) de gouvernance et d'animation de la politique biodiversité",
            "environnement",
        ),
        ("Chargé(e) de contentieux administratif", "juridique"),
        ("Chargé(e) de mission recrutements et mobilités", "rh"),
        ("Chargé(e) de communication digitale, webmestre", "communication"),
        ("Référent(e) budgétaire et comptable régional(e)", "finances"),
        (
            "Ingénieur(e) data, développement, maintenance et administration",
            "numerique",
        ),
        ("Chargé(e) de mission stratégie achat", "achats"),
        ("Chargé(e) de mission certificats d'économies d'énergie", "environnement"),
        ("Chargé(e) de suivi des audits et contrôles externes", "audit"),
        ("Chef(fe) de projet qualité de l'air intérieur et santé", "environnement"),
        ("Assistant(e) de direction", "pilotage"),
        ("Chargé(e) de mission sortie de statut de déchets", "environnement"),
    ],
)

_CULTURE = _organisme(
    "culture",
    1947,
    [
        ("Conservateur(trice) régional(e) de l'archéologie", "culture"),
        (
            "Chargé(e) de conservation et de restauration sur monuments historiques",
            "culture",
        ),
        ("Conseiller(ère) pour le théâtre et les arts associés", "culture"),
        ("Chargé(e) de médiation culturelle pour le public scolaire", "culture"),
        ("Chargé(e) d'études juridiques", "juridique"),
        ("Régisseur(se) d'œuvres", "culture"),
        ("Chargé(e) d'analyse budgétaire", "finances"),
        ("Chargé(e) de communication et de développement des publics", "communication"),
        ("Chef(fe) de produit / Product Owner", "numerique"),
        ("Gestionnaire carrière et paie", "rh"),
        ("Chef(fe) du service du livre et de la lecture", "culture"),
        ("Instructeur(trice)-contrôleur(se) en architecture et urbanisme", "culture"),
        ("Acheteur(se) public(que)", "achats"),
        ("Secrétaire général(e) adjoint(e)", "pilotage"),
        ("Archiviste mutualisé(e)", "culture"),
    ],
)

_CENTRE_POMPIDOU = _organisme(
    "centre-pompidou",
    1948,
    [
        ("Adjoint(e) au/à la chef(fe) du service des expositions", "culture"),
        ("Régisseur(se) d'œuvres d'art", "culture"),
        ("Chargé(e) d'action éducative et de production", "culture"),
        ("Chargé(e) de développement et partenariats", "communication"),
        ("Responsable du pôle vidéo", "communication"),
        ("Chargé(e) de gestion administrative et juridique", "juridique"),
        ("Directeur(trice) juridique et financier(ère)", "finances"),
        ("Attaché(e) de presse", "communication"),
        ("Monteur(se)-encadreur(se) des dessins d'architecture", "culture"),
        ("Gestionnaire administratif(ve) des ressources humaines", "rh"),
        ("Régisseur(se) technique d'exposition", "culture"),
        ("Graphiste junior", "communication"),
        ("Chef(fe) du service du dialogue social et qualité de vie au travail", "rh"),
        ("Assistant(e) archivage et gestion documentaire RH", "rh"),
        ("Chargé(e) de prospective et d'innovation sociale", "pilotage"),
    ],
)

_PREMIER_MINISTRE = _organisme(
    "premier-ministre",
    1949,
    [
        ("Consultant(e) en transformation et organisation", "pilotage"),
        ("Chargé(e) de rédaction juridique", "juridique"),
        ("Secrétaire général(e) adjoint(e)", "pilotage"),
        ("Chargé(e) de relations presse", "communication"),
        ("Ingénieur(e) cybersécurité IA LLM", "numerique"),
        ("Chef(fe) de projet RH", "rh"),
        ("Chargé(e) du dialogue social", "rh"),
        ("Chargé(e) de mission maîtrise des risques et contrôle interne", "audit"),
        ("Data architecte", "numerique"),
        (
            "Juriste acheteur(se) spécialisé(e) en marchés industriels et immobiliers",
            "achats",
        ),
        ("Chef(fe) du bureau du budget", "finances"),
        ("Responsable de projet éditorial", "communication"),
        ("Ingénieur(e) réseaux et télécommunications", "numerique"),
        ("Gestionnaire paie et indemnités", "rh"),
        ("Assistant(e) de direction", "pilotage"),
    ],
)

_COUR_DES_COMPTES = _organisme(
    "cour-des-comptes",
    1950,
    [
        ("Vérificateur(trice) des juridictions financières", "audit"),
        ("Magistrat(e) rapporteur(e)", "audit"),
        (
            "Auditeur(trice) financier(ère), certification des comptes de l'État",
            "audit",
        ),
        ("Auditeur(trice) du numérique", "audit"),
        ("Consultant(e) analyste fonctionnel(le)", "numerique"),
        ("Secrétaire général(e) adjoint(e)", "pilotage"),
        ("Greffier(ère) de section", "juridique"),
        ("Responsable de la communication interne", "communication"),
        ("Chargé(e) de recrutement", "rh"),
        ("Assistant(e) de publications", "communication"),
        (
            "Adjoint(e) au/à la directeur(trice) du patrimoine et de la logistique",
            "pilotage",
        ),
        ("Chef(fe) du département du budget et du contrôle de gestion", "finances"),
        ("Gestionnaire coordinateur(trice) paie", "rh"),
        ("Technicien(ne) environnement du poste de travail", "numerique"),
        (
            "Responsable de la mission projets, méthodes et outils, données sociales",
            "rh",
        ),
    ],
)

_TRAVAIL_SOLIDARITES = _organisme(
    "travail-solidarites",
    1951,
    [
        ("Inspecteur(trice) du travail", "solidarites"),
        ("Conseiller(ère) en insertion professionnelle", "solidarites"),
        ("Chargé(e) de missions transversales autonomie", "solidarites"),
        ("Chargé(e) de mission lutte contre la pauvreté", "solidarites"),
        ("Juriste droit public", "juridique"),
        ("Chef(fe) de projet animation de la politique du handicap", "solidarites"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Responsable éditorial(e) web", "communication"),
        ("Data scientist", "numerique"),
        ("Chargé(e) de recrutement", "rh"),
        ("Chargé(e) de mission hébergement d'urgence", "solidarites"),
        (
            "Adjoint(e) au/à la chef(fe) du bureau de la protection de l'enfance",
            "solidarites",
        ),
        ("Responsable de l'achat public", "achats"),
        ("Secrétaire assistant(e) de direction", "pilotage"),
        ("Chargé(e) administratif(ve) du dialogue social", "rh"),
    ],
)

_DGAFP = _organisme(
    "dgafp",
    1952,
    [
        ("Chargé(e) d'études juridiques, codification", "juridique"),
        ("Chargé(e) d'études salariales", "rh"),
        ("Chef(fe) du pôle SIRH", "numerique"),
        ("Chargé(e) de mission lutte contre les discriminations et diversité", "rh"),
        ("Gestionnaire de formation", "rh"),
        (
            "Chef(fe) du département de la donnée et des systèmes d'information",
            "numerique",
        ),
        ("Chargé(e) du contentieux", "juridique"),
        ("Chargé(e) de communication marque employeur", "communication"),
        ("Adjoint(e) au/à la chef(fe) du département protection sociale", "rh"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Chef(fe) du département des formations et de la scolarité", "rh"),
        (
            "Chef(fe) de projet adjoint(e) métier d'un chatbot RH à base d'IA",
            "numerique",
        ),
        ("Assistant(e) informatique", "numerique"),
        ("Acheteur(se) public(que)", "achats"),
        ("Gestionnaire administratif(ve)", "pilotage"),
    ],
)

_ECONOMIE_FINANCES = _organisme(
    "economie-finances",
    1953,
    [
        (
            "Économiste sur la décarbonation, l'énergie et la politique industrielle",
            "finances",
        ),
        (
            "Comptable public(que), responsable du service des impôts des entreprises",
            "finances",
        ),
        ("Chef(fe) de projets aides d'État et transition verte", "finances"),
        ("Responsable du pôle expertise fiscale et foncière", "finances"),
        ("Juriste en droit des sociétés, fusions et acquisitions", "juridique"),
        (
            "Correspondant(e) budgétaire des emplois et crédits de personnels",
            "finances",
        ),
        (
            "Auditeur(trice) interne senior de l'instrument financier européen SAFE",
            "audit",
        ),
        ("Responsable des relations presse", "communication"),
        ("Data scientist", "numerique"),
        ("Gestionnaire des ressources humaines", "rh"),
        ("Gestionnaire financier(ère)", "finances"),
        ("Acheteur(se) de prestations intellectuelles confirmé(e)", "achats"),
        ("Assistant(e) de direction", "pilotage"),
        ("Concepteur(trice) développeur(se) fullstack", "numerique"),
        (
            "Délégué(e) à l'information stratégique et à la sécurité économiques",
            "finances",
        ),
    ],
)

_CAISSE_DES_DEPOTS = _organisme(
    "caisse-des-depots",
    1954,
    [
        ("Chargé(e) de développement territorial prêteur", "finances"),
        ("Chef(fe) de projets inter-régimes", "rh"),
        ("Analyste conformité bancaire et financière", "audit"),
        ("Juriste financier(ère)", "juridique"),
        ("Analyste risques financiers", "audit"),
        (
            "Responsable en structuration de projets immobilier et infrastructures",
            "finances",
        ),
        (
            "Chargé(e) d'opérations consignations administratives et judiciaires",
            "finances",
        ),
        ("Chargé(e) de communication éditoriale", "communication"),
        ("Business analyst SI back-office finance", "numerique"),
        ("Responsable prospective et pilotage des ressources humaines", "rh"),
        ("Acheteur(se)", "achats"),
        ("Responsable data gouvernance et qualité", "numerique"),
        ("Chargé(e) de mission engagements environnementaux", "environnement"),
        ("Assistant(e) de direction", "pilotage"),
        ("Directeur(trice) territorial(e) au handicap", "solidarites"),
    ],
)

SPECS_DEMO: dict[str, SpecOrganisme] = {
    spec.cle: spec
    for spec in (
        _TRANSITION_ECOLOGIQUE,
        _CULTURE,
        _CENTRE_POMPIDOU,
        _PREMIER_MINISTRE,
        _COUR_DES_COMPTES,
        _TRAVAIL_SOLIDARITES,
        _DGAFP,
        _ECONOMIE_FINANCES,
        _CAISSE_DES_DEPOTS,
    )
}
