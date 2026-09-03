from django.db.models import TextChoices


class DomaineFonctionnel(TextChoices):
    ACHAT = ("ACH", "Achat")
    AGRICULTURE = ("AGR", "Agriculture")
    AMENAGEMENT_DEVELOPPEMENT_DURABLE_TERRITOIRE = (
        "AMT",
        "Aménagement et développement durable du territoire",
    )
    ANIMATION_JEUNESSE_SPORTS = ("ASP", "Animation, jeunesse et sports")
    BATIMENT = ("BAT", "Bâtiment")
    COMMUNICATION = ("COM", "Communication")
    ORGANISATION_CONTROLE_EVALUATION = ("CTL", "Organisation, contrôle et évaluation")
    CULTURE_PATRIMOINE = ("CUL", "Culture et Patrimoine")
    DEFENSE = ("DEF", "Défense")
    DIRECTION_PILOTAGE_POLITIQUES_PUBLIQUES = (
        "DIR",
        "Direction et pilotage des politiques publiques",
    )
    LECTURE_PUBLIQUE_DOCUMENTATION = ("DOC", "Lecture publique et Documentation")
    ENSEIGNEMENT_FORMATION = ("ENS", "Enseignement et Formation")
    ENVIRONNEMENT = ("ENV", "Environnement")
    FINANCES_PUBLIQUES = ("FIP", "Finances publiques")
    GESTION_BUDGETAIRE_FINANCIERE = ("GBF", "Gestion budgétaire et financière")
    RESSOURCES_HUMAINES = ("GRH", "Ressources humaines")
    INTERNATIONAL = ("INT", "International")
    AFFAIRES_JURIDIQUES = ("JUR", "Affaires juridiques")
    JUSTICE = ("JUS", "Justice")
    INTERVENTIONS_TECHNIQUES_LOGISTIQUES = (
        "LOG",
        "Interventions techniques et logistiques",
    )
    MEDICAL_PARAMEDICAL = ("MED", "Médical et paramédical")
    NUMERIQUE = ("NUM", "Numérique")
    RECHERCHE = ("RCH", "Recherche")
    RENSEIGNEMENT = ("REN", "Renseignement")
    PREVENTION_CONSEIL_PILOTAGE_SANTE = (
        "SAN",
        "Prévention, conseil et pilotage en santé",
    )
    SECURITE = ("SEC", "Sécurité")
    SOCIAL_ENFANCE_FAMILLE = ("SOC", "Social, enfance et famille")
    TRANSPORTS = ("TRA", "Transports")
    RELATION_USAGER = ("USA", "Relation à l'usager")
