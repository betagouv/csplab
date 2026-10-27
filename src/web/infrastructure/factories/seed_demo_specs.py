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
        ("Chargé(e) de mission biodiversité", "environnement"),
        ("Chef(fe) de projet adaptation au changement climatique", "environnement"),
        ("Inspecteur(trice) des installations classées", "environnement"),
        ("Chargé(e) d'études mobilités durables", "environnement"),
        ("Juriste en droit de l'environnement", "juridique"),
        ("Gestionnaire RH de proximité", "rh"),
        ("Chargé(e) de communication digitale", "communication"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Chef(fe) de projet SIG", "numerique"),
        ("Acheteur(se) public(que)", "achats"),
        ("Chargé(e) de mission économie circulaire", "environnement"),
        ("Adjoint(e) au/à la chef(fe) du bureau budgétaire", "finances"),
        ("Chargé(e) de mission prévention des risques naturels", "environnement"),
        ("Assistant(e) de direction", "pilotage"),
        ("Chargé(e) de mission rénovation énergétique des bâtiments", "environnement"),
    ],
)

_CULTURE = _organisme(
    "culture",
    1947,
    [
        ("Chargé(e) de mission patrimoine monumental", "culture"),
        ("Chargé(e) d'études archéologie préventive", "culture"),
        ("Conseiller(ère) livre et lecture", "culture"),
        ("Chargé(e) de mission éducation artistique et culturelle", "culture"),
        ("Juriste propriété littéraire et artistique", "juridique"),
        ("Chargé(e) de mission spectacle vivant", "culture"),
        ("Gestionnaire budgétaire et comptable", "finances"),
        ("Chargé(e) de communication institutionnelle", "communication"),
        ("Chef(fe) de projet numérique culturel", "numerique"),
        ("Responsable des ressources humaines", "rh"),
        ("Conservateur(trice) du patrimoine, archives", "culture"),
        ("Chargé(e) de mission musées de France", "culture"),
        ("Acheteur(se) marchés de travaux", "achats"),
        ("Secrétaire général(e) adjoint(e) de DRAC", "pilotage"),
        ("Conseiller(ère) architecture", "culture"),
    ],
)

_CENTRE_POMPIDOU = _organisme(
    "centre-pompidou",
    1948,
    [
        ("Chargé(e) de production d'expositions", "culture"),
        ("Régisseur(se) d'œuvres", "culture"),
        ("Chargé(e) des publics et de la médiation", "culture"),
        ("Chargé(e) de mécénat et partenariats", "communication"),
        ("Chef(fe) de projet billetterie et CRM", "numerique"),
        ("Juriste droits d'auteur et contrats", "juridique"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Chargé(e) de communication éditoriale", "communication"),
        ("Documentaliste, bibliothèque Kandinsky", "culture"),
        ("Gestionnaire paie et carrières", "rh"),
        ("Attaché(e) de conservation, arts graphiques", "culture"),
        ("Acheteur(se) public(que)", "achats"),
        ("Administrateur(trice) systèmes et réseaux", "numerique"),
        ("Chargé(e) de programmation cinéma", "culture"),
        ("Responsable logistique des expositions", "pilotage"),
    ],
)

_PREMIER_MINISTRE = _organisme(
    "premier-ministre",
    1949,
    [
        ("Chargé(e) de mission coordination interministérielle", "pilotage"),
        ("Rédacteur(trice) juridique, légistique", "juridique"),
        ("Chef(fe) de projet transformation publique", "pilotage"),
        ("Chargé(e) de veille et d'analyse médias", "communication"),
        ("Développeur(se) full stack", "numerique"),
        ("Chargé(e) d'études prospective", "pilotage"),
        ("Gestionnaire RH et formation", "rh"),
        ("Chargé(e) d'évaluation des politiques publiques", "audit"),
        ("Responsable de la sécurité des systèmes d'information", "numerique"),
        ("Acheteur(se) prestations intellectuelles", "achats"),
        ("Conseiller(ère) budgétaire", "finances"),
        ("Chargé(e) de communication interministérielle", "communication"),
        ("Chef(fe) de produit numérique", "numerique"),
        ("Juriste droit public des affaires", "juridique"),
        ("Assistant(e) de cabinet", "pilotage"),
    ],
)

_COUR_DES_COMPTES = _organisme(
    "cour-des-comptes",
    1950,
    [
        ("Vérificateur(trice) des juridictions financières", "audit"),
        ("Rapporteur(e) extérieur(e)", "audit"),
        ("Auditeur(trice) des comptes de l'État", "audit"),
        ("Chargé(e) d'évaluation des politiques publiques", "audit"),
        ("Data scientist, contrôle des comptes publics", "numerique"),
        ("Assistant(e) de vérification", "audit"),
        ("Juriste contentieux financier", "juridique"),
        ("Chargé(e) de communication et relations presse", "communication"),
        ("Gestionnaire des ressources humaines", "rh"),
        ("Documentaliste juridique", "juridique"),
        ("Expert(e) certification des comptes", "audit"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Acheteur(se) public(que)", "achats"),
        ("Chef(fe) de projet informatique", "numerique"),
        ("Responsable des services généraux", "pilotage"),
    ],
)

_TRAVAIL_SOLIDARITES = _organisme(
    "travail-solidarites",
    1951,
    [
        ("Inspecteur(trice) du travail", "solidarites"),
        ("Chargé(e) de mission insertion professionnelle", "solidarites"),
        ("Chargé(e) de mission politiques de l'autonomie", "solidarites"),
        ("Chargé(e) d'études statistiques emploi", "solidarites"),
        ("Juriste droit du travail", "juridique"),
        ("Chargé(e) de mission lutte contre la pauvreté", "solidarites"),
        ("Gestionnaire budgétaire", "finances"),
        ("Chargé(e) de communication", "communication"),
        ("Chef(fe) de projet SI santé-social", "numerique"),
        ("Conseiller(ère) mobilité carrière", "rh"),
        ("Chargé(e) de mission égalité professionnelle", "solidarites"),
        ("Chargé(e) de mission handicap et emploi", "solidarites"),
        ("Acheteur(se) public(que)", "achats"),
        ("Assistant(e) de direction", "pilotage"),
        ("Chargé(e) de mission dialogue social", "rh"),
    ],
)

_DGAFP = _organisme(
    "dgafp",
    1952,
    [
        ("Chargé(e) d'études statut général des fonctionnaires", "juridique"),
        ("Chargé(e) de mission politique de rémunération", "rh"),
        ("Chef(fe) de projet SIRH interministériel", "numerique"),
        ("Chargé(e) de mission égalité et diversité", "rh"),
        ("Chargé(e) de mission formation professionnelle", "rh"),
        ("Statisticien(ne) emploi public", "numerique"),
        ("Juriste droit de la fonction publique", "juridique"),
        ("Chargé(e) de communication marque employeur", "communication"),
        ("Chargé(e) de mission dialogue social", "rh"),
        ("Contrôleur(se) de gestion", "finances"),
        ("Chargé(e) de mission encadrement supérieur", "rh"),
        ("Chargé(e) de mission santé et sécurité au travail", "rh"),
        ("Chef(fe) de projet recrutement", "rh"),
        ("Acheteur(se) public(que)", "achats"),
        ("Assistant(e) de direction", "pilotage"),
    ],
)

_ECONOMIE_FINANCES = _organisme(
    "economie-finances",
    1953,
    [
        ("Analyste financier(ère)", "finances"),
        ("Chargé(e) de mission politique fiscale", "finances"),
        ("Économiste conjoncturiste", "finances"),
        ("Contrôleur(se) des finances publiques", "finances"),
        ("Juriste droit de la concurrence", "juridique"),
        ("Chargé(e) de mission participations de l'État", "finances"),
        ("Auditeur(trice) interne", "audit"),
        ("Chargé(e) de communication", "communication"),
        ("Développeur(se) applications fiscales", "numerique"),
        ("Gestionnaire RH", "rh"),
        ("Chargé(e) de mission commerce extérieur", "finances"),
        ("Acheteur(se) public(que)", "achats"),
        ("Chargé(e) de mission politique industrielle", "finances"),
        ("Data analyst", "numerique"),
        ("Chef(fe) du bureau budget", "finances"),
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
    )
}
