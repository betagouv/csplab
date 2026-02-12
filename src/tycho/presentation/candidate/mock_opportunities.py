"""Mock opportunities for development when no real data is available."""

MOCK_OPPORTUNITIES: list[dict[str, str | list[str]]] = [
    {
        "type": "concours",
        "title": "Ingénieurs des systèmes d'information et de communication",
        "description": "Ingénieur des systèmes d'information et de communication",
        "metier": "Ingénieur des systèmes d'information et de communication",
        "concours_type": ["Externe", "Interne"],
        "category": "Catégorie A",
        "category_value": "a",
        "category_icon": "fr-icon-award-line",
        "versant": "Fonction publique d'État",
        "versant_value": "FPE",
        "versant_icon": "fr-icon-government-line",
        "job_type": "",
        "contract_icon": "fr-icon-briefcase-line",
        "url": "#",
    },
    {
        "type": "offer",
        "title": "Chargé des renseignements des usagers en droit du travail",
        "description": (
            "Au sein d'un service situé dans les locaux de la cité administrative, "
            "le ou la chargé(e) des renseignements en droit du travail assurera "
            "le renseignement des salariés sur la réglementation en droit du travail, "
            "de l'emploi et de la formation professionnelle."
        ),
        "metier": "Chargée / Chargé du renseignement en droit du travail",
        "location": "Centre-Val de Loire, Loir-et-Cher",
        "category": "Catégorie B",
        "category_value": "b",
        "category_icon": "fr-icon-award-line",
        "versant": "Fonction publique d'État",
        "versant_value": "FPE",
        "versant_icon": "fr-icon-government-line",
        "job_type": "Titulaire / Contractuel",
        "contract_icon": "fr-icon-briefcase-line",
        "url": "#",
    },
    {
        "type": "concours",
        "title": "Secrétaires administratifs de l'intérieur et de l'outre-mer",
        "description": (
            "Secrétaire administratif de l'intérieur et de l'outre-mer "
            "de classe normale"
        ),
        "metier": "Secrétaire administratif",
        "concours_type": ["Externe", "Interne", "Troisième concours"],
        "category": "Catégorie B",
        "category_value": "b",
        "category_icon": "fr-icon-award-line",
        "versant": "Fonction publique d'État",
        "versant_value": "FPE",
        "versant_icon": "fr-icon-government-line",
        "job_type": "",
        "contract_icon": "fr-icon-briefcase-line",
        "url": "#",
    },
    {
        "type": "offer",
        "title": "Chef de projet transformation numérique",
        "description": (
            "Piloter les projets de transformation numérique au sein de la direction "
            "du numérique. Coordonner les équipes techniques et métiers pour assurer "
            "la bonne exécution des projets."
        ),
        "metier": "Chef de projet SI",
        "location": "Île-de-France, Paris",
        "category": "Catégorie A",
        "category_value": "a",
        "category_icon": "fr-icon-award-line",
        "versant": "Fonction publique d'État",
        "versant_value": "FPE",
        "versant_icon": "fr-icon-government-line",
        "job_type": "Titulaire",
        "contract_icon": "fr-icon-briefcase-line",
        "url": "#",
    },
    {
        "type": "offer",
        "title": "Développeur full-stack Python/Django",
        "description": (
            "Concevoir et développer des applications web au sein de l'incubateur "
            "de services numériques. Participer à la conception des architectures "
            "techniques et à la mise en place des bonnes pratiques de développement."
        ),
        "metier": "Développeur / Développeuse",
        "location": "Île-de-France, Paris",
        "category": "Catégorie A",
        "category_value": "a",
        "category_icon": "fr-icon-award-line",
        "versant": "Fonction publique d'État",
        "versant_value": "FPE",
        "versant_icon": "fr-icon-government-line",
        "job_type": "Contractuel",
        "contract_icon": "fr-icon-briefcase-line",
        "url": "#",
    },
]
