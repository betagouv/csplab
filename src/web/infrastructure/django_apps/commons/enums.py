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
    TEAM_NOTES = "nb_notes_equipe", "Notes pour l'équipe"
    PERSONAL_NOTES = "nb_notes_personnelles", "Notes personnelles"
    SCREENED_APPLICATIONS_WITH_TEAM_NOTE = (
        "nb_candidatures_premier_tri_avec_note_equipe",
        "Candidatures au-delà du premier tri avec une note pour l'équipe",
    )
    TEAM_MESSAGES = "nb_messages_equipe", "Messages de l'équipe"
    CANDIDAT_MESSAGES = "nb_messages_candidats", "Messages des candidats"
    SCREENED_APPLICATIONS_WITH_TEAM_MESSAGE = (
        "nb_candidatures_premier_tri_avec_message_equipe",
        "Candidatures au-delà du premier tri avec un message de l'équipe",
    )
    CONVERSATIONS = "nb_conversations", "Conversations"
    CONVERSATIONS_OPENED_BY_CANDIDAT = (
        "nb_conversations_ouvertes_par_candidat",
        "Conversations ouvertes par un candidat",
    )
    APPLICATIONS_WITH_CONVERSATION = (
        "nb_candidatures_avec_conversation",
        "Candidatures avec au moins une conversation",
    )
    APPLICATIONS_WITH_SEVERAL_CONVERSATIONS = (
        "nb_candidatures_plusieurs_conversations",
        "Candidatures avec plusieurs conversations",
    )
    DOCUMENTS_ADDED_BY_MEMBER = (
        "nb_documents_ajoutes_par_membre",
        "Documents ajoutés par un membre",
    )
    CANDIDAT_ATTACHMENTS = (
        "nb_pieces_jointes_candidats",
        "Pièces jointes envoyées par les candidats",
    )
    SCREENED_APPLICATIONS_WITH_COMPLETED_FILE = (
        "nb_candidatures_premier_tri_dossier_complete",
        "Candidatures au-delà du premier tri au dossier complété dans l'outil",
    )
