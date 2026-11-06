from django.db import models


class Canal(models.TextChoices):
    ADMIN = "admin", "Admin Django"
    JWT = "jwt", "API (JWT)"
    APIKEY = "apikey", "API (clé d'API)"
    PROCONNECT = "proconnect", "ProConnect"


class Resultat(models.TextChoices):
    SUCCES = "succes", "Succès"
    ECHEC = "echec", "Échec"


class Metric(models.TextChoices):
    PUBLISHED_OFFERS = "nb_offres_publiees", "Offres publiées"
    ARCHIVED_OFFERS = "nb_offres_archivees", "Offres archivées"
    RECEIVED_APPLICATIONS = "nb_candidatures_recues", "Candidatures reçues"
    WITHDRAWN_APPLICATIONS = "nb_candidatures_retirees", "Candidatures retirées"
    APPLICATIONS_TO_PROCESS = "nb_candidatures_a_traiter", "Candidatures à traiter"
    PROCESSED_APPLICATIONS = "nb_candidatures_traitees", "Candidatures traitées"
    APPLICATIONS_PAST_FIRST_SCREENING = (
        "nb_candidatures_au_dela_premier_tri",
        "Candidatures au-delà du premier tri",
    )
    REFUSED_APPLICATIONS = "nb_candidatures_refusees", "Candidatures refusées"
    SELECTED_APPLICATIONS = (
        "nb_candidatures_selectionnees",
        "Candidatures sélectionnées",
    )
    RECRUTEMENTS = "nb_recrutements", "Recrutements"
    OPEN_ORGANISMES = "nb_organismes_ouverts", "Organismes ouverts"
    ORGANISME_SUPERVISEURS = (
        "nb_membres_organisme_superviseur",
        "Membres d'organisme superviseurs",
    )
    ORGANISME_AGENTS = "nb_membres_organisme_agent", "Membres d'organisme agents"
    RECRUTEMENT_RESPONSABLES = (
        "nb_membres_recrutement_responsable",
        "Membres de recrutement responsables",
    )
    RECRUTEMENT_RECRUTEURS = (
        "nb_membres_recrutement_recruteur",
        "Membres de recrutement recruteurs",
    )
    RECRUTEMENT_CONTRIBUTEURS = (
        "nb_membres_recrutement_contributeur",
        "Membres de recrutement contributeurs",
    )
    CANDIDAT_ACCOUNTS = "nb_comptes_candidats", "Comptes candidats"
