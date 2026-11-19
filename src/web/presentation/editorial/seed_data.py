"""Contenu éditorial initial (POC), importé par la commande seed_editorial."""

_URL = "https://choisirleservicepublic.gouv.fr/"
_IMG = "candidate/images/"
_PDL = "candidate/images/territory-pdl/"
_NOR = "candidate/images/territory-normandie/"
_ADVICE_IMG = "candidate/images/advice/"
_ADVICE_URL = "https://choisirleservicepublic.gouv.fr/conseils/"

_SEEPH_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non sem vel ante "
    "consequat pulvinar. Nam consequat gravida velit non sollicitudin. Cras "
    "tristique in magna nec molestie. Morbi consectetur neque odio, et vestibulum "
    "est egestas non. Praesent iaculis nisi justo, quis volutpat mi lacinia "
    "vitae. Aliquam erat volutpat. Nunc a orci id tortor vehicula posuere. "
    "Praesent sed mollis sapien, eget auctor augue. Etiam aliquet dictum euismod. "
    "Phasellus eleifend nisi ac porta pretium. Praesent dapibus nibh justo, nec "
    "pellentesque nunc efficitur et. In hac habitasse platea dictumst. Phasellus "
    "et augue id tortor condimentum ultricies id sit amet lorem. Cras dui urna, "
    "volutpat sit amet rutrum sed, laoreet ut mauris. Nulla at luctus mi, at "
    "consectetur felis. Nam ut nisi elementum turpis tristique tempor vel vitae "
    "arcu. Pellentesque dui urna, interdum nec dapibus id, ullamcorper tempor "
    "turpis. Suspendisse sit amet lorem quis massa vulputate convallis molestie "
    "sed tellus. Nulla pharetra facilisis porttitor. In ligula tellus, rhoncus "
    "eget est ac, dignissim laoreet felis. Nunc facilisis venenatis odio nec "
    "tincidunt. Phasellus malesuada urna sit amet massa vestibulum, ut cursus "
    "dolor ullamcorper. Vestibulum lobortis dolor sed dignissim maximus. Vivamus "
    "et purus ullamcorper, ornare odio sed, faucibus nulla. Aliquam sodales arcu "
    "et tortor pulvinar posuere. Donec et sollicitudin est, ornare euismod mi. "
    "Nunc nec iaculis nisl, quis pharetra massa. In pellentesque luctus sem, sed "
    "fringilla magna lobortis eget. Mauris tempus risus mi, a facilisis massa "
    "pharetra vel. Curabitur imperdiet tortor non justo malesuada, sed iaculis "
    "enim porta. Nulla facilisi. Praesent et turpis "
)

_FEATURED_NEWS = [
    {
        "badge": "Événement",
        "title": "Semaine européenne pour l'emploi des personnes handicapées 2026 : "
        "une semaine pour favoriser l'inclusion professionnelle",
        "description": _SEEPH_TEXT,
        "url": "https://www.semaine-emploi-handicap.com/edition-2026-seeph2026",
        "image": _IMG + "news/semaine-handicap.jpg",
    },
    {
        "badge": "Métier",
        "title": "Sandra Renoir, lauréate du concours de secrétaire administratif "
        "au MAASA : « Il ne faut pas hésiter à se lancer ! »",
        "url": _URL,
        "image": _IMG + "news/sandra-renoir.jpg",
    },
]


_NEWS = [
    {
        "badge": "Diversité",
        "title": "Cyril, ancien militaire reconverti, s'engage pour l'inclusion "
        "et l'emploi des personnes en situation de handicap",
        "description": "Cyril travaille depuis près de 20 ans au ministère des "
        "Armées et des Anciens combattants : après une carrière militaire,…",
        "url": _URL,
        "image": _IMG + "news/cyril.png",
    },
    {
        "badge": "Concours",
        "title": "Cinq raisons de devenir professeur",
        "description": "Être professeur, c'est transmettre des savoirs et des "
        "valeurs, accompagner chaque élève vers la réussite et contribuer à…",
        "url": _URL,
        "image": _IMG + "news/professeur.jpg",
    },
    {
        "badge": "Événement",
        "title": "Mois de l'innovation publique 2026 : découvrez les initiatives "
        "qui transforment le service public",
        "description": "Du 2 au 30 novembre 2026, le Mois de l'innovation publique "
        "revient pour sa 13e édition. Organisé par la Direction interministérielle…",
        "url": _URL,
        "image": _IMG + "news/innovation.webp",
    },
    {
        "badge": "Concours",
        "title": "Ouverture du concours Technicien supérieur d'études et de "
        "fabrications de 3ème classe (TSEF3)",
        "description": "Vous souhaitez mettre vos compétences techniques au service "
        "de la Défense ? Exercer un métier où votre savoir-faire contribue…",
        "url": _URL,
        "image": _IMG + "news/concours-senat.png",
    },
]


_TERRITORIES = [
    ("Auvergne-Rhône-Alpes", "auvergne-rhone-alpes"),
    ("Bourgogne-Franche-Comté", "bourgogne-franche-comte"),
    ("Bretagne", "bretagne"),
    ("Centre-Val de Loire", "centre-val-de-loire"),
    ("Corse", "corse"),
    ("Grand Est", "grand-est"),
    ("Guadeloupe", "guadeloupe"),
    ("Guyane", "guyane"),
    ("Hauts-de-France", "hauts-de-france"),
    ("Île-de-France", "ile-de-france"),
    ("La Réunion", "reunion"),
    ("Martinique", "martinique"),
    ("Mayotte", "mayotte"),
    ("Normandie", "normandie"),
    ("Nouvelle-Aquitaine", "nouvelle-aquitaine"),
    ("Occitanie", "occitanie"),
    ("Pays de la Loire", "pays-de-la-loire"),
    ("Provence-Alpes-Côte d'Azur", "provence-alpes-cote-dazur"),
]


_TERRITORY_NEWS = {
    "normandie": {
        "marque-employeur": {
            "title": "Zoom sur la marque employeur des services de l'Etat en Normandie",
            "badge": "Marque employeur",
            "description": "Face aux enjeux en matière d'attractivité auxquels les "
            "services de l'État sont confrontés, le préfet de la région Normandie a "
            "souhaité créer une marque employeur permettant de mettre en avant, sous "
            "une même bannière, les opportunités mais aussi les atouts de ce versant "
            "de la fonction publique, encore trop souvent méconnu et stigmatisé.",
            "url": "https://www.prefectures-regions.gouv.fr/normandie/"
            "Rejoignez-nous/Rejoignez-nous",
            "image": _NOR + "Logo-4-800x450.jpg",
        },
    },
}

_TERRITORY_PAGES = {
    "pays-de-la-loire": {
        "name": "Pays de la Loire",
        "title": "La région Pays de la Loire",
        "image": _PDL + "Pays-de-la-Loire.png",
        "highlights": [
            {
                "title": "Une mobilité professionnelle en vue ? "
                "Une solution logement existe forcément !",
                "tags": ["Fonction Publique d'Etat", "Mobilité"],
                "date": "29/07/2026",
                "image": _PDL + "Visuel_Baraque.jpg",
            },
            {
                "title": "Les rencontres de l'emploi public 2026, c'est fini !",
                "tags": ["Employeur", "Événement", "Métier", "Mobilité", "Recrutement"],
                "date": "3/04/2026",
                "image": _PDL + "REP26_Zoom_16_9-400x400.jpg",
            },
            {
                "title": "Préparez votre insertion dans la fonction publique "
                "avec l'Ipag de Nantes",
                "tags": ["Candidat", "Concours"],
                "date": "3/04/2026",
                "image": _PDL + "IPAG1-400x408.jpg",
            },
            {
                "title": "Préparez votre concours administratif avec l'Ipag de Nantes",
                "tags": ["Concours"],
                "date": "3/04/2026",
                "image": _PDL + "IPAG2-400x500.jpg",
            },
        ],
        "links": [
            {
                "title": "Découvrez les grandes tendances de l'emploi public "
                "en Pays de la Loire",
                "text": "En Pays de la Loire, un fort renouvellement des effectifs "
                "à prévoir qui ouvre de beaux possibles professionnels !",
                "url": "https://www.insee.fr/fr/statistiques/8061128",
                "image": _PDL + "Image_Etude_INSEE_PDL_2024-800x450.jpg",
            },
            {
                "title": "Agents publics de l'Etat en Pays de la Loire, pour vous "
                "faciliter la vie, toute l'offre disponible en matière d'action "
                "sociale",
                "text": "Il y a forcément une prestation qui vous concerne, que vous "
                "soyez agent public de l'État, actif ou retraité, avec ou sans "
                "enfant !",
                "url": "https://srias-paysdelaloire.fr/",
                "image": _PDL + "Image_SRIAS_PDL.jpg",
            },
            {
                "title": "La Préfecture des Pays de la Loire et de Loire-Atlantique",
                "text": "Rendez-vous sur la page Linkedin de la Préfecture des Pays "
                "de la Loire et de Loire-Atlantique, chaque lundi c'est le "
                "#Monday Motivation...",
                "url": "https://www.linkedin.com/company/prefecture-de-loire-atlantique/",
                "image": _PDL + "prefecture_de_loire_atlantique_logo.jpeg",
            },
        ],
    },
    "normandie": {
        "name": "Normandie",
        "title": "La région Normandie",
        "image": _NOR + "Normandie.png",
        "highlights": [
            {
                "title": "Zoom sur la marque employeur des services de l'Etat "
                "en Normandie",
                "tags": [],
                "date": "17/08/2026",
                "image": _NOR + "Logo-4-800x450.jpg",
            },
            {
                "title": "Fonction Publique Hospitalière (FPH) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
            {
                "title": "Fonction Publique Territoriale (FPT) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
            {
                "title": "Fonction Publique d'État (FPE) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
        ],
        "assets_title": "Nos atouts territoriaux",
        "assets": [
            {
                "title": "Un patrimoine reconnu",
                "image": _NOR + "BestJobers_NA_1110_218_HD-1200px-600x400.jpg",
                "caption": "Palais Bénédictine, Fécamp. BestJobers – "
                "Normandie Attractivité",
                "text": "La région Normandie bénéficie d'un patrimoine historique "
                "et d'une identité culturelle reconnue, portés par des sites "
                "emblématiques comme le Mont-Saint-Michel, les falaises "
                "d'Étretat, les plages du débarquement ou encore les jardins de "
                "Giverny, qui en font une région particulièrement touristique et "
                "riche. De même, les nombreux musées et centres historiques des "
                "villes composant la région représentent autant de lieux "
                "différents à découvrir.",
            },
            {
                "title": "Un territoire tourné vers l'emploi et l'innovation",
                "image": _NOR + "Toshiba3-1200px-600x400.jpg",
                "caption": "Toshiba Dieppe. Logistique Seine-Normandie",
                "text": "Au-delà de son image touristique, la région Normandie est "
                "aussi une région d'activité et de production, qui bénéficie "
                "d'un tissu économique diversifié ainsi que d'une position "
                "stratégique au niveau national, notamment au niveau maritime "
                "avec les grands ports de Rouen et du Havre. Elle se distingue "
                "par ses avancées en matière technologique, notamment dans les "
                "secteurs maritimes et spatiaux, ou encore celui de la santé.",
            },
            {
                "title": "Une région à taille humaine",
                "image": _NOR
                + "Enjoyed-by-artists-Copyright-The-Explorers-1200px-600x338.jpg",
                "caption": "Veules-les-Roses. Valentin PACAUT – The Explorers",
                "text": "La région se distingue par sa capacité à proposer un cadre "
                "de vie accessible et équilibré, et une variété de paysages "
                "inégalable. Elle est composée aussi bien de grands centres "
                "urbains que de communes rurales, de littoral maritime que "
                "d'espaces verts. Ses villes moyennes et la variété de ses "
                "espaces permettent de construire des parcours de vie différents "
                "sans renoncer à la proximité des services et emplois.",
            },
            {
                "title": "Un cadre de vie de qualité",
                "image": _NOR + "Rouen-photo911.fr-62-1200px-600x400.jpg",
                "caption": "Balade en centre-ville de Rouen. Studio 911 – "
                "Normandie Attractivité",
                "text": "La Normandie séduit par sa qualité de vie, entre son "
                "patrimoine naturel et historique et ses zones d'activité. "
                "Elle dispose aussi d'une offre culturelle dense et variée, au "
                "travers d'évènements comme l'Armada, les carnavals de Rouen et "
                "de Caen ou encore ses nombreux festivals.",
            },
        ],
        "state_title": "L'administration territoriale de l'État (ATE) en région "
        "Normandie",
        "state_text": "L'administration territoriale de l'État est caractérisée par "
        "ses services déconcentrés, qui assurent le relais au niveau local des "
        "décisions prises par l'administration centrale. Placés généralement sous "
        "l'autorité d'un préfet (de région ou de département), ils veillent à la "
        "mise en œuvre des politiques nationales au niveau territorial. Retrouvez "
        "ci-dessous les différents services de l'État en région Normandie :",
        "state_links": [
            "L'organisation de l'État au sein de la région Normandie",
            "L'organisation de l'État au sein des départements",
            "L'organisation de l'État hors-périmètre ATE",
        ],
        "figures_title": "La région en chiffres",
        "figures": [
            ("29 900 km²", "de superficie totale"),
            ("≈ 3 341 312", "habitants au 1er janvier 2025 (Insee)"),
            (
                "5 départements",
                "Seine-Maritime (76), Orne (61), Eure (27), Manche (50), Calvados (14)",
            ),
            ("2 644", "communes"),
            ("5,4 %", "du territoire métropolitain"),
            ("640 km", "de côtes le long de la Manche"),
            (
                "2 grands ports",
                (
                    "maritimes du Havre et de Rouen, débouché de Paris vers le "
                    "commerce maritime mondial"
                ),
            ),
            (
                "≈ 265 064 agents publics",
                (
                    "fin 2023 : ≈ 99 203 territoriale, ≈ 104 600 État, "
                    "≈ 71 600 hospitalière"
                ),
            ),
        ],
        "employers": 2,
        "links": [
            {
                "title": "Vie Publique",
                "text": "Mieux comprendre le fonctionnement de l'administration.",
                "url": "https://www.vie-publique.fr/fiches/administration",
            },
            {
                "title": "L'annuaire du service public",
                "text": "Trouvez des informations sur n'importe quelle administration.",
                "url": "https://lannuaire.service-public.gouv.fr/",
            },
            {
                "title": "Répertoire des métiers de la fonction publique",
                "text": "Trouvez n'importe quel emploi public.",
                "url": "https://www.fonction-publique.gouv.fr/toutes-les-"
                "publications/repertoire-commun-des-metiers-de-la-fonction-publique",
            },
            {
                "title": "INSEE : panorama de l'emploi public Normandie",
                "text": "Étude sur la démographie de la fonction publique normande.",
                "url": "https://www.insee.fr/statistiques/7674091",
            },
        ],
        "links_title": "Les ressources utiles",
    },
}


_ADVICE_THEMES = {
    "entretien": "Entretien",
    "handicap": "Handicap",
    "interet": "Je m'intéresse à la fonction publique",
    "agent": "Je suis agent public",
}

_ADVICE = [
    {
        "title": "Parole d'expert – Conseils pour une photo de CV réussie",
        "text": "L'idée de mentionner un handicap sur un CV ou lors d'un entretien "
        "peut être source d'appréhension. « Vais-je être jugé ? », « Ma "
        "candidature sera-t-elle écartée ? ». Ces craintes...",
        "image": "Image1.png",
        "themes": ["entretien", "interet"],
    },
    {
        "title": "Témoignages : l'immersion professionnelle, un dispositif au "
        "service des projets de mobilité des agents",
        "text": "Agents publics ! Vous êtes dans une démarche de mobilité et "
        "souhaitez confirmer votre projet ou découvrir un métier ? Avez-vous "
        "pensé à l'immersion professionnelle ? Découvrez notre témoignage...",
        "image": "Periode-dimmersion-professionnelle1-800x445.png",
        "themes": ["agent"],
    },
    {
        "title": "Réussir sa prise de poste (webinaire en replay)",
        "text": "Comment imaginez-vous les premiers jours dans votre nouvel "
        "emploi ? Cette question peut vous être posée en entretien et vous "
        "pouvez également - vous-même - avoir besoin de vous projeter pour...",
        "image": "PFRH-GE-Onboarding-800x445.png",
        "themes": ["entretien", "agent"],
    },
    {
        "title": "Parole d'experte : réseauter pour mieux rebondir !",
        "text": "Vous souhaitez donner une nouvelle trajectoire à votre parcours "
        "professionnel, changer de poste, de métier ? ...",
        "image": "DISPOSITIFS-800x445.webp",
        "themes": ["agent", "interet"],
    },
    {
        "title": "Parole d'experte – situation de handicap : en parler dans sa "
        "candidature ?",
        "text": "L'idée de mentionner un handicap sur un CV ou lors d'un entretien "
        "peut être source d'appréhension. « Vais-je être jugé ? », « Ma "
        "candidature sera-t-elle écartée ? ». Ces craintes...",
        "image": "AdobeStock_53166648R-scaled-1-800x445.jpg",
        "themes": ["handicap", "entretien"],
    },
    {
        "title": "Parole d'experte : les bonnes pratiques de l'enquête métier",
        "text": "Vous souhaitez mieux connaître un métier, une fonction, un "
        "secteur d'activité et confronter vos représentations à la réalité du "
        "terrain ? Une solution : rencontrer un professionnel ! ...",
        "image": "illustr-parole-de-CMC-conseil-Etat-1.png",
        "themes": ["interet"],
    },
    {
        "title": "Parole d'expert : préparer un entretien ne s'improvise pas !",
        "text": "Que ce soit pour un recrutement, une mobilité ou une "
        "reconversion, un entretien nécessite de la méthode, de la prise de "
        "recul… et un peu d'entraînement. En tant que Conseiller Mobilité...",
        "image": "parole-expert-H-PFRH.jpg",
        "themes": ["entretien"],
    },
    {
        "title": "Identifier le fil rouge de votre parcours",
        "text": "Il existe plusieurs moments clés dans votre carrière où vous "
        "devrez présenter votre parcours : lors de la construction d'un projet "
        "professionnel ou lors d'un entretien de recrutement....",
        "image": "Picto_Mobilite.svg",
        "themes": ["entretien", "agent"],
    },
    {
        "title": "Comment parler d'une réussite professionnelle ?",
        "text": "Parler de vos réussites professionnelles tout en ne donnant pas "
        "l'impression d'être prétentieux vous semble être un exercice délicat ? "
        "C'est pourtant une démarche incontournable dans le cadre...",
        "image": "Picto_Entretien.svg",
        "themes": ["entretien"],
    },
]
