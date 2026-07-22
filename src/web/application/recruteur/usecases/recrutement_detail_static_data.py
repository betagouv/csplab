from typing import Any

# ---------------------------------------------------------------------------
# Données statiques — TODO: remplacer par une vraie source de données
# ---------------------------------------------------------------------------

STATIC_RECRUTEMENT_DETAIL: dict[str, Any] = {
    "offer_id": "aaaaaaaa-0001-0001-0001-000000000001",
    "intitule": "Chargé de mission numérique",
    "date_publication": "2025-06-22T10:00:00Z",
    "localisation": {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "11",
        "departement": "75",
        "localisation_label": "Paris 8e arrondissement",
        "latitude": 48.8748,
        "longitude": 2.3070,
    },
    "organisme_recruteur": {
        "nom": "Mairie de Paris",
        "siret": "21750001600019",
    },
    "categorie_offre": "A",
    "etapes": [
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000001",
            "nom": "Réception des candidatures",
            "categorie": "ENTREE",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000001",
                    "date_soumission": "2025-06-10T09:15:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000001",
                        "nom": "Dupont",
                        "prenom": "Alice",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000002",
                    "date_soumission": "2025-06-11T14:30:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000002",
                        "nom": "Martin",
                        "prenom": "Bruno",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000003",
                    "date_soumission": "2025-06-12T11:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000003",
                        "nom": "Leroy",
                        "prenom": "Camille",
                    },
                    "date_derniere_activite": "2025-06-12T11:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000004",
                    "date_soumission": "2025-06-13T08:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000004",
                        "nom": "Moreau",
                        "prenom": "David",
                    },
                    "date_derniere_activite": "2025-06-13T08:45:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000002",
            "nom": "Présélection",
            "categorie": "EN_COURS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000005",
                    "date_soumission": "2025-06-08T10:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000005",
                        "nom": "Bernard",
                        "prenom": "Élise",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000006",
                    "date_soumission": "2025-06-09T16:20:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000006",
                        "nom": "Petit",
                        "prenom": "François",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000007",
                    "date_soumission": "2025-06-07T13:10:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000007",
                        "nom": "Roux",
                        "prenom": "Géraldine",
                    },
                    "date_derniere_activite": "2025-06-12T11:00:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000003",
            "nom": "Entretien",
            "categorie": "EN_COURS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000008",
                    "date_soumission": "2025-06-05T09:30:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000008",
                        "nom": "Simon",
                        "prenom": "Hélène",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000009",
                    "date_soumission": "2025-06-04T11:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000009",
                        "nom": "Michel",
                        "prenom": "Ivan",
                    },
                    "date_derniere_activite": "2025-06-13T08:45:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000004",
            "nom": "Candidatures refusées",
            "categorie": "REFUS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000010",
                    "date_soumission": "2025-06-03T14:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000010",
                        "nom": "Thomas",
                        "prenom": "Juliette",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000011",
                    "date_soumission": "2025-06-02T10:15:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000011",
                        "nom": "Richard",
                        "prenom": "Kevin",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000005",
            "nom": "Candidature acceptée",
            "categorie": "ACCEPTE",
            "candidatures": [],
        },
    ],
}

# Lookup {offer_id: detail} pour simulation de la BDD
STATIC_RECRUTEMENTS_DETAIL_BY_ID: dict[str, dict[str, Any]] = {
    STATIC_RECRUTEMENT_DETAIL["offer_id"]: STATIC_RECRUTEMENT_DETAIL,
}
