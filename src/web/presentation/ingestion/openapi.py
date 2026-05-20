from drf_spectacular.utils import OpenApiExample

CONCOURS_UPLOAD_DESCRIPTION = (
    "Permet d'uploader un fichier CSV contenant des données de concours GRECO "
    "afin de les importer dans le système.\n\n"
    "**Format attendu :**\n"
    "- Encodage : UTF-8\n"
    "- Séparateur : point-virgule (`;`)\n\n"
    "**Colonnes obligatoires :**\n"
    "- `N° NOR` — identifiant unique de l'arrêté (utilisé comme clé d'upsert)\n"
    "- `Corps`\n"
    "- `Grade`\n"
    "- `Ministère`\n\n"
    "**Traitement :**\n"
    "- Validation ligne par ligne selon le schéma `ConcoursRowSchema`\n"
    "- Les lignes valides sont créées ou mises à jour (upsert par `N° NOR`)\n"
    "- Les lignes invalides sont ignorées et remontées dans `validation_errors`\n\n"
    "**Codes de retour :**\n"
    "- `201 Created` — au moins une ligne valide a été traitée avec succès\n"
    "- `400 Bad Request` — fichier absent, format invalide, ou aucune ligne valide\n"
    "- `401 Unauthorized` — token JWT manquant ou invalide\n"
    "- `500 Internal Server Error` — erreur inattendue côté serveur\n\n"
    "**Authentification :** Token JWT requis."
)

CONCOURS_UPLOAD_EXAMPLES = [
    OpenApiExample(
        "Success - full import",
        summary="Toutes les lignes sont valides",
        description="Aucune erreur de validation, toutes les lignes ont été importées.",
        value={
            "status": "success",
            "message": "Successfully processed 5185 valid concours records",
            "total_rows": 5185,
            "valid_rows": 5185,
            "invalid_rows": 0,
            "created": 5185,
            "updated": 0,
            "validation_errors": None,
        },
        response_only=True,
        status_codes=["201"],
    ),
    OpenApiExample(
        "Success - partial import with errors",
        summary="Import partiel avec des lignes invalides",
        description=(
            "Certaines lignes ont échoué la validation mais les lignes valides "
            "ont quand même été persistées. Le champ `validation_errors` détaille "
            "chaque ligne rejetée."
        ),
        value={
            "status": "success",
            "message": "Successfully processed 5162 valid concours records",
            "total_rows": 5185,
            "valid_rows": 5162,
            "invalid_rows": 23,
            "created": 5100,
            "updated": 62,
            "validation_errors": [
                {"row": 4, "error": "Le champ 'Corps' est requis"},
                {"row": 17, "error": "Le champ 'Grade' est requis"},
                {
                    "row": 156,
                    "error": "Le champ 'date_ouverture' doit être au format JJ/MM/AAAA",
                },
            ],
        },
        response_only=True,
        status_codes=["201"],
    ),
    OpenApiExample(
        "Success - update only",
        summary="Mise à jour de concours existants",
        description="Toutes les lignes correspondent à des enregistrements existants",
        value={
            "status": "success",
            "message": "Successfully processed 120 valid concours records",
            "total_rows": 120,
            "valid_rows": 120,
            "invalid_rows": 0,
            "created": 0,
            "updated": 120,
            "validation_errors": None,
        },
        response_only=True,
        status_codes=["201"],
    ),
    OpenApiExample(
        "Error - no file provided",
        summary="Aucun fichier dans la requête",
        description="Le champ `file` est absent du corps de la requête multipart.",
        value={"error": "No file provided"},
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "Error - wrong file type",
        summary="Fichier non CSV",
        description="Le fichier uploadé n'a pas l'extension `.csv`.",
        value={"error": "File must be a CSV"},
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "Error - no valid rows",
        summary="Aucune ligne valide après validation",
        description=(
            "Toutes les lignes ont échoué la validation. "
            "Aucune donnée n'a été persistée."
        ),
        value={
            "error": "No valid rows found",
            "validation_errors": [
                {"row": 1, "error": "Le champ 'N° NOR' est requis"},
                {"row": 2, "error": "Le champ 'Corps' est requis"},
                {"row": 3, "error": "Le champ 'Grade' doit être >= 1"},
            ],
        },
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "Error - malformed CSV",
        summary="Fichier CSV mal formé",
        description=(
            "Le fichier ne peut pas être parsé,"
            "vérifiez le séparateur (`;`) et l'encodage (UTF-8)."
        ),
        value={"error": "CSV parsing error"},
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "Error - invalid token",
        summary="Token JWT invalide ou expiré",
        description="Le token dans le header `Authorization` est invalide ou expiré.",
        value={
            "detail": "Le jeton fourni n'est pas valide.",
            "code": "token_not_valid",
            "messages": [
                {
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token is invalid or expired",
                }
            ],
        },
        response_only=True,
        status_codes=["401"],
    ),
    OpenApiExample(
        "Error - unexpected server error",
        summary="Erreur serveur inattendue",
        description="Une erreur inattendue s'est produite côté serveur.",
        value={"error": "Unexpected error"},
        response_only=True,
        status_codes=["500"],
    ),
]

LIST_OFFERS_DESCRIPTION = """
# API de consultation des offres d'emploi de la Fonction Publique

Cette API retourne la liste de offres correspondant à une recherche selon les 2
critères suivants :

- Candidature active / archivée
- Référence externe de la candidature contient une chaîne de caractère spécifique

Cette API est à l’usage exclusif des personnes autorisées.

# Permissions

L’utilisation de cette API nécessite un token d’autorisation spécifique à chaque
utilisateur.

# Limitations

L’interrogation de cette API est limitée à 120 appels par minute et par utilisateur.
"""

LIST_SOURCES_DESCRIPTION = """
# API de consultation des sources d'ingestion

Cette API retourne la liste complète des sources configurées sans pagination.

# Permissions

L'utilisation de cette API nécessite une clé API dans le header `Authorization`.
Format attendu : `Api-Key <clé>`.
"""

LIST_SOURCES_EXAMPLES = [
    OpenApiExample(
        "Success - list of sources",
        summary="Liste des sources",
        description="La liste complète des sources d'ingestion configurées.",
        value=[
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "type": "talentsoft",
                "client_id_front": "client_front_123",
                "client_id_back": "client_back_456",
                "base_url": "https://example.talentsoft.com",
            }
        ],
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Error - missing or invalid API key",
        summary="Clé API absente ou invalide",
        description=(
            "Le header `Authorization` est absent ou la clé API est invalide. "
            "Format attendu : `Api-Key <clé>`."
        ),
        value={"detail": "Invalid API key."},
        response_only=True,
        status_codes=["401"],
    ),
    OpenApiExample(
        "Error - unexpected server error",
        summary="Erreur serveur inattendue",
        description="Une erreur inattendue s'est produite côté serveur.",
        value={"error": "Unexpected error"},
        response_only=True,
        status_codes=["500"],
    ),
]

LIST_OFFERS_EXAMPLES = [
    OpenApiExample(
        "Success - active offers",
        summary="Liste des offres d'emploi actives",
        description=(
            "Les offres d'emploi sans date d'archivagesont retournées paginées"
        ),
        value={
            "external_id": "Versant_FPE-2026-999999",
            "title": "Responsable de la Division des Affaires Financières H/F",
            "organization": "Ecole Nationale Supérieure de Techniques Avancées (ENSTA)",
            "contract_type": "TITULAIRE_CONTRACTUEL",
            "category": "A",
            "publication_date": "2026-04-17T14:44:49.873000+00:00",
            "offer_url": "https://test.com/offre-emploi/2026-999999/",
            "archived_at": None,
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Success - archived offers",
        summary="Liste des offres d'emploi archivées",
        description=(
            "Les offres d'emploi avec une date d'archivagesont retournées paginées"
        ),
        value={
            "external_id": "Versant_FPE-2026-999999",
            "title": "Responsable de la Division des Affaires Financières H/F",
            "organization": "Ecole Nationale Supérieure de Techniques Avancées (ENSTA)",
            "contract_type": "TITULAIRE_CONTRACTUEL",
            "category": "A",
            "publication_date": "2026-04-17T14:44:49.873000+00:00",
            "offer_url": "https://test.com/offre-emploi/2026-999999/",
            "archived_at": "2026-05-17T12:42:42.873000+00:00",
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Error - invalid token",
        summary="Token JWT invalide ou expiré",
        description="Le token dans le header `Authorization` est invalide ou expiré.",
        value={
            "detail": "Le jeton fourni n'est pas valide.",
            "code": "token_not_valid",
            "messages": [
                {
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token is invalid or expired",
                }
            ],
        },
        response_only=True,
        status_codes=["401"],
    ),
    OpenApiExample(
        "Error - unexpected server error",
        summary="Erreur serveur inattendue",
        description="Une erreur inattendue s'est produite côté serveur.",
        value={"error": "Unexpected error"},
        response_only=True,
        status_codes=["500"],
    ),
]
