from drf_spectacular.utils import OpenApiExample

_API_COMMON_FOOTER = """
Cette API est à l'usage exclusif des personnes autorisées.

# Permissions

L'utilisation de cette API nécessite un token d'autorisation spécifique à chaque
utilisateur.

# Limitations

L'interrogation de cette API est limitée à 120 appels par minute et par utilisateur.
"""

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

LIST_OFFERS_DESCRIPTION = (
    """
# API de consultation des offres d'emploi de la Fonction Publique

Cette API retourne la liste de offres correspondant à une recherche selon les 2
critères suivants :

- Candidature active / archivée
- Référence externe de la candidature contient une chaîne de caractère spécifique

"""
    + _API_COMMON_FOOTER
)

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

LIST_METIERS_DESCRIPTION = (
    """
# API de consultation des métiers de la Fonction Publique

Cette API retourne la liste paginées des métiers. Les métiers peuvent être filtrés
selon leur code de domaine fonctionnel (`domain`).

"""
    + _API_COMMON_FOOTER
)

LIST_METIERS_EXAMPLES = [
    OpenApiExample(
        "Success - all",
        summary="Liste de tous les métiers",
        description=("Les métiers sont retournés paginés"),
        value={
            "libelle": "Cheffe / Chef de projet politique de la ville",
            "description": (
                "Mettre en oeuvre les orientations stratégiques en matière"
                "de développement social et de redynamisation des espaces urbains des"
                "Quartiers Politique de la Ville"
            ),
            "domaine_fonctionnel_code": "AMT",
            "versants": ["FPT"],
            "activites": [
                (
                    "Animer et participer aux instances techniques et"
                    "de pilotage de la politique de la ville"
                ),
                (
                    "Instruire les programmations d'actions :"
                    "suivi administratif, financier et opérationnel"
                ),
                (
                    "Assurer un rôle de conseil et d'information auprès"
                    "des différents interlocuteurs"
                ),
            ],
            "conditions_particulieres": [],
            "offer_family_code": "ERAMT001",
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Success - filtered",
        summary="Liste des métiers correspondants à un code domaine fonctionnel",
        description=(
            "Les métiers possédant ce code domaine fonctionnle sont retournés paginés"
        ),
        value={
            "libelle": "Personne ressource en santé et protection animales",
            "description": (
                "Mobilise sa compétence dans la gestion et le suivi de la santé et de"
                "la protection animale en appui aux services territoriaux de l'État"
            ),
            "domaine_fonctionnel_code": "AGR",
            "versants": ["FPE"],
            "activites": [
                (
                    "Mettre en oeuvre la compétence technique et scientifique dans"
                    "son domaine de compétence par un appui ponctuel à un service"
                    "départemental confronté à une situation particulière"
                ),
                (
                    "Apporter un appui dans l'élaboration des normes,"
                    "des instructions et des méthodes d'inspection"
                ),
            ],
            "conditions_particulieres": ["Déplacements nationaux et internationaux"],
            "offer_family_code": "ERAGR001",
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Error - malformed payload",
        summary="Données invalides",
        description=("Les données passées dans le payload sont incorrectes"),
        value={"error": "string"},
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
