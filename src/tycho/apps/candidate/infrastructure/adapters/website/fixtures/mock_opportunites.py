"""Mock data for opportunites.

TODO: Remove when AnalyzeCVUsecase is implemented.
"""

MOCK_OPPORTUNITES = [
    {
        "id": 1,
        "title": "Adjoint au chargé de mission transports et mobilité",
        "type": "emploi",
        "type_label": None,
        "location": "paris",
        "location_display": "Paris",
        "public_service_branch": "Fonction publique d'État",
        "branch_key": "etat",
        "category": "A",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Adjoint administratif de l'état",
    },
    {
        "id": 2,
        "title": "Concours Adjoint administratif des administrations de l'État",
        "type": "concours",
        "type_label": "Concours interne",
        "location": None,
        "location_display": None,
        "public_service_branch": "Fonction publique d'État",
        "branch_key": "etat",
        "category": "A",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Adjoint administratif de l'état",
    },
    {
        "id": 3,
        "title": "Chargé(e) de mission transformation numérique",
        "type": "emploi",
        "type_label": None,
        "location": "lyon",
        "location_display": "Lyon",
        "public_service_branch": "Fonction publique Territoriale",
        "branch_key": "territoriale",
        "category": "A",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Chargé de mission",
    },
    {
        "id": 4,
        "title": "Infirmier en soins généraux",
        "type": "emploi",
        "type_label": None,
        "location": "marseille",
        "location_display": "Marseille",
        "public_service_branch": "Fonction publique Hospitalière",
        "branch_key": "hospitaliere",
        "category": "A",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Infirmier",
    },
    {
        "id": 5,
        "title": "Concours de rédacteur territorial",
        "type": "concours",
        "type_label": "Concours externe",
        "location": None,
        "location_display": None,
        "public_service_branch": "Fonction publique Territoriale",
        "branch_key": "territoriale",
        "category": "B",
        "recruitment_level": "Niveau de recrutement",
        "intitule_poste": "Rédacteur territorial",
    },
]

MOCK_OPPORTUNITE_DETAIL = {
    "id": 1,
    "title": "Adjoint au chargé de mission transports et mobilité",
    "type": "emploi",
    "type_label": None,
    "employer": "Préfecture de Paris",
    "location": "Paris",
    "public_service_branch": "Fonction publique d'État",
    "branch_key": "etat",
    "category": "A",
    "recruitment_level": "Niveau de recrutement",
    "intitule_poste": "Adjoint administratif de l'état",
    "description": (
        "Cadre de direction au sein des collectivités locales, "
        "l'attaché territorial participe à l'élaboration et à la mise en œuvre "
        "des politiques publiques locales."
    ),
    "external_url": "https://choisirleservicepublic.gouv.fr/",
}
