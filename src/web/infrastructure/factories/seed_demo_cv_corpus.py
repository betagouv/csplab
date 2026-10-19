from typing import TypedDict


class Experience(TypedDict):
    titre: str
    employeur: str
    description: str


class Formation(TypedDict):
    diplome: str
    etablissement: str


class PosteCorpus(TypedDict):
    mission: str
    profil_recherche: str
    profil: list[str]
    formations: list[Formation]
    experiences_directes: list[Experience]
    experiences_voisines: list[Experience]
    competences_poste: list[str]
    competences_voisines: list[str]


def _exp(titre: str, employeur: str, description: str) -> Experience:
    return {"titre": titre, "employeur": employeur, "description": description}


def _form(diplome: str, etablissement: str) -> Formation:
    return {"diplome": diplome, "etablissement": etablissement}


_EXPERIENCES_TRANSVERSES = [
    _exp(
        "Chargé(e) de mission auprès du directeur général des services",
        "Communauté d'agglomération du Grand Chalon",
        "Suivi des dossiers transversaux, préparation des instances et des "
        "arbitrages, coordination des directions opérationnelles.",
    ),
    _exp(
        "Consultant(e) en organisation",
        "Cabinet de conseil en management public",
        "Accompagnement de collectivités et d'établissements publics dans "
        "leurs projets de transformation et de conduite du changement.",
    ),
    _exp(
        "Attaché(e) d'administration",
        "Ministère de l'Intérieur, secrétariat général",
        "Rédaction de notes, préparation de réunions interministérielles et "
        "suivi budgétaire des crédits du programme.",
    ),
    _exp(
        "Chef(fe) de projet événementiel",
        "Agence d'organisation de grands événements sportifs",
        "Pilotage du planning, coordination des prestataires et relation "
        "avec les partenaires institutionnels.",
    ),
]

_COMPETENCES_TRANSVERSES = [
    "Conduite de projet et animation d'équipes pluridisciplinaires",
    "Rédaction de notes de synthèse et d'éléments de langage",
    "Préparation et animation de comités de pilotage",
    "Maîtrise des outils bureautiques et collaboratifs",
    "Sens du service public et devoir de réserve",
    "Capacité d'analyse et esprit de synthèse",
]

CORPUS: dict[str, PosteCorpus] = {
    "Secrétaire général(e)": {
        "mission": (
            "Piloter les fonctions support de la délégation (ressources "
            "humaines, budget, achats, logistique, affaires juridiques) et "
            "garantir le bon fonctionnement de l'organisation."
        ),
        "profil_recherche": (
            "Cadre expérimenté(e) des fonctions support, habitué(e) au "
            "pilotage budgétaire et au management d'équipes."
        ),
        "profil": [
            (
                "Secrétaire général(e) adjoint(e) depuis six ans, j'ai piloté les "
                "fonctions support d'une direction de 300 agents."
            ),
            (
                "Manager des fonctions support, attaché(e) à la qualité du "
                "dialogue social et à la maîtrise de la dépense."
            ),
        ],
        "formations": [
            _form(
                "Master Administration publique", "Université Paris 1 Panthéon-Sorbonne"
            ),
            _form(
                "Cycle supérieur de management", "Institut national du service public"
            ),
            _form("Master Gestion des ressources humaines", "IAE de Lyon"),
            _form("Diplôme de Sciences Po", "Sciences Po Bordeaux"),
        ],
        "experiences_directes": [
            _exp(
                "Secrétaire général(e) adjoint(e)",
                (
                    "Direction régionale de l'environnement, de l'aménagement "
                    "et du logement"
                ),
                "Encadrement des pôles RH, budget et logistique ; pilotage du "
                "plan de charge et du dialogue de gestion.",
            ),
            _exp(
                "Responsable du pôle ressources",
                "Agence régionale de santé",
                "Préparation et exécution d'un budget de 40 M EUR, conduite de "
                "la réorganisation des services supports.",
            ),
            _exp(
                "Chef(fe) du bureau des affaires générales",
                "Préfecture de région",
                "Gestion des marchés publics, des moyens généraux et du "
                "contrôle interne comptable.",
            ),
            _exp(
                "Directeur(rice) des ressources humaines",
                "Établissement public territorial",
                "Pilotage de la masse salariale, de la GPEC et des relations "
                "avec les organisations syndicales.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Pilotage budgétaire et dialogue de gestion",
            "Management des fonctions support",
            "Commande publique et exécution des marchés",
            "Gestion des ressources humaines et dialogue social",
            "Contrôle interne et maîtrise des risques",
            "Conduite de réorganisations",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Conseiller(ère) héritage": {
        "mission": (
            "Concevoir et suivre la stratégie d'héritage des Jeux : "
            "pérennisation des équipements, programmes sportifs et impact "
            "durable pour les territoires."
        ),
        "profil_recherche": (
            "Expérience des politiques sportives ou de l'évaluation de "
            "politiques publiques, goût du travail partenarial."
        ),
        "profil": [
            (
                "Spécialiste des politiques sportives, j'accompagne depuis huit "
                "ans les territoires dans la valorisation de leurs équipements."
            ),
            (
                "Chargé(e) d'évaluation de politiques publiques, intéressé(e) par "
                "l'impact durable des grands événements."
            ),
        ],
        "formations": [
            _form("Master Management du sport", "Université Paris-Saclay"),
            _form("Master Évaluation des politiques publiques", "Sciences Po Lyon"),
            _form("Licence STAPS", "Université de Bourgogne"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission héritage",
                "Comité d'organisation d'un championnat du monde",
                "Définition des indicateurs d'impact et suivi des engagements "
                "des collectivités hôtes.",
            ),
            _exp(
                "Responsable des politiques sportives",
                "Conseil départemental",
                "Programmation des équipements, appels à projets et "
                "accompagnement des clubs.",
            ),
            _exp(
                "Chargé(e) d'études",
                "Agence nationale du sport",
                "Analyse de l'usage des équipements et élaboration de "
                "recommandations de reconversion.",
            ),
            _exp(
                "Chef(fe) de projet Terre de Jeux",
                "Ville de Saint-Denis",
                "Animation du label, mobilisation des associations et "
                "programmation d'événements sportifs.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Politiques publiques du sport",
            "Évaluation d'impact et construction d'indicateurs",
            "Reconversion et exploitation d'équipements",
            "Animation de partenariats avec les collectivités",
            "Connaissance du mouvement sportif",
            "Montage d'appels à projets",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Chargé(e) de mission infrastructures": {
        "mission": (
            "Suivre l'avancement des infrastructures et des sites, coordonner "
            "les maîtres d'ouvrage et alerter sur les risques de calendrier."
        ),
        "profil_recherche": (
            "Formation d'ingénieur, expérience de la maîtrise d'ouvrage "
            "publique ou du pilotage de grands chantiers."
        ),
        "profil": [
            (
                "Ingénieur(e) en génie civil, j'ai conduit des opérations "
                "d'aménagement pour des maîtres d'ouvrage publics."
            ),
            (
                "Chef(fe) de projet travaux, rompu(e) au pilotage de calendriers "
                "contraints et à la coordination d'intervenants."
            ),
        ],
        "formations": [
            _form("Diplôme d'ingénieur génie civil", "École des Ponts ParisTech"),
            _form(
                "Diplôme d'ingénieur ENTPE",
                "École nationale des travaux publics de l'État",
            ),
            _form("Master Aménagement et urbanisme", "Université Gustave Eiffel"),
        ],
        "experiences_directes": [
            _exp(
                "Responsable d'opérations",
                "Société de livraison des ouvrages olympiques",
                "Suivi de la construction de sites, maîtrise des coûts et des "
                "délais, reporting au comité de pilotage.",
            ),
            _exp(
                "Chef(fe) de projet maîtrise d'ouvrage",
                "Établissement public d'aménagement",
                "Conduite d'opérations d'aménagement de la programmation à la "
                "réception des ouvrages.",
            ),
            _exp(
                "Ingénieur(e) travaux",
                "Direction interdépartementale des routes",
                "Pilotage de chantiers routiers et coordination des "
                "entreprises et des concessionnaires de réseaux.",
            ),
            _exp(
                "Chargé(e) d'opérations",
                "Métropole du Grand Paris",
                "Suivi d'équipements sportifs et culturels en construction, "
                "gestion des avenants.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Maîtrise d'ouvrage publique et loi MOP",
            "Planification et suivi de chantiers",
            "Analyse des risques calendaires",
            "Maîtrise des coûts d'opération",
            "Coordination des intervenants",
            "Lecture de plans et de pièces techniques",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Conseiller(ère) juridique / affaires législatives": {
        "mission": (
            "Sécuriser juridiquement les décisions de la délégation, suivre "
            "les textes législatifs et réglementaires et préparer les "
            "projets de textes."
        ),
        "profil_recherche": (
            "Juriste de droit public, expérience de la légistique ou du "
            "travail parlementaire appréciée."
        ),
        "profil": [
            (
                "Juriste de droit public, j'ai rédigé et suivi des projets de "
                "textes au sein d'une direction des affaires juridiques."
            ),
            (
                "Conseiller(ère) juridique, à l'aise avec la procédure "
                "parlementaire et la sécurisation des actes administratifs."
            ),
        ],
        "formations": [
            _form(
                "Master Droit public des affaires", "Université Paris 2 Panthéon-Assas"
            ),
            _form("Master Droit public approfondi", "Université de Montpellier"),
            _form(
                "Certificat d'aptitude à la profession d'avocat",
                "École de formation du barreau",
            ),
        ],
        "experiences_directes": [
            _exp(
                "Juriste légiste",
                "Secrétariat général du Gouvernement",
                "Relecture de projets de décrets, préparation des saisines du "
                "Conseil d'État et suivi des consultations.",
            ),
            _exp(
                "Conseiller(ère) parlementaire",
                "Cabinet ministériel",
                "Suivi des débats, préparation des amendements et des réponses "
                "aux questions écrites.",
            ),
            _exp(
                "Juriste contentieux",
                "Direction des affaires juridiques d'un ministère",
                "Rédaction de mémoires devant les juridictions administratives "
                "et conseil aux directions métiers.",
            ),
            _exp(
                "Administrateur(rice) adjoint(e)",
                "Assemblée nationale, service des commissions",
                "Préparation des travaux de commission et rédaction de "
                "rapports législatifs.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Légistique et rédaction de textes normatifs",
            "Procédure parlementaire",
            "Droit administratif et contentieux",
            "Veille juridique",
            "Sécurisation des actes et des marchés",
            "Droit de la commande publique",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Conseiller(ère) finances et garanties de l’État": {
        "mission": (
            "Suivre les engagements financiers et les garanties de l’État "
            "liés aux Jeux, préparer les arbitrages budgétaires et le "
            "dialogue avec la direction du budget."
        ),
        "profil_recherche": (
            "Expérience des finances publiques, de la LOLF ou du contrôle de "
            "gestion ; rigueur et sens de l'analyse financière."
        ),
        "profil": [
            (
                "Spécialiste des finances publiques, j'ai suivi les engagements "
                "et les garanties de l’État au sein d'une direction financière."
            ),
            (
                "Analyste budgétaire, habitué(e) au dialogue avec la direction du "
                "budget et au suivi des risques financiers de l’État."
            ),
        ],
        "formations": [
            _form("Master Finances publiques", "Université Paris 1 Panthéon-Sorbonne"),
            _form("Master Contrôle de gestion et audit", "IAE d'Aix-Marseille"),
            _form("Diplôme de l'ESSEC, majeure finance", "ESSEC Business School"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission garanties",
                "Direction générale du Trésor",
                "Instruction des demandes de garantie, analyse des risques et "
                "suivi du portefeuille d'engagements.",
            ),
            _exp(
                "Analyste budgétaire",
                "Direction du budget",
                "Suivi d'un programme budgétaire, préparation des conférences "
                "budgétaires et des lois de finances.",
            ),
            _exp(
                "Contrôleur(se) de gestion",
                "Opérateur de l'État",
                "Construction du budget, suivi de l'exécution et des "
                "indicateurs de performance.",
            ),
            _exp(
                "Auditeur(rice) financier(ère)",
                "Cour des comptes, chambre régionale",
                "Contrôle des comptes et de la gestion d'organismes publics, "
                "rédaction de rapports d'observations.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Finances publiques et LOLF",
            "Analyse des risques financiers",
            "Préparation des lois de finances",
            "Suivi des garanties et engagements hors bilan",
            "Contrôle de gestion",
            "Modélisation financière sous tableur",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Conseiller(ère) sécurité et ordre public": {
        "mission": (
            "Coordonner avec le ministère de l'Intérieur et les préfectures la "
            "préparation du dispositif de sécurité des sites et des "
            "célébrations."
        ),
        "profil_recherche": (
            "Expérience de la sécurité intérieure, de la gestion de crise ou "
            "de la sécurisation de grands événements."
        ),
        "profil": [
            (
                "Officier(ère) de gendarmerie, j'ai planifié la sécurisation de "
                "grands rassemblements et piloté des cellules de crise."
            ),
            (
                "Spécialiste de la gestion de crise, habitué(e) à la coordination "
                "interservices en préfecture."
            ),
        ],
        "formations": [
            _form("Master Sécurité intérieure", "Université Toulouse Capitole"),
            _form(
                "Formation d'officier",
                "École des officiers de la gendarmerie nationale",
            ),
            _form("Master Gestion des risques et des crises", "Université de Nîmes"),
        ],
        "experiences_directes": [
            _exp(
                "Chef(fe) du bureau de l'ordre public",
                "Préfecture de police",
                "Planification des services d'ordre et coordination des forces "
                "lors de grands événements.",
            ),
            _exp(
                "Officier(ère) adjoint(e) au commandant de groupement",
                "Gendarmerie nationale",
                "Conduite d'opérations de sécurisation et de gestion d'événements "
                "majeurs.",
            ),
            _exp(
                "Chargé(e) de mission sécurité des grands événements",
                "Délégation interministérielle aux grands événements sportifs",
                "Préparation des concepts de sécurité et suivi des exercices de crise.",
            ),
            _exp(
                "Directeur(rice) de cabinet adjoint(e)",
                "Préfecture de département",
                "Gestion de la permanence, des crises et de la sécurité publique.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Planification de dispositifs de sécurité",
            "Gestion de crise et conduite d'exercices",
            "Coordination police, gendarmerie et secours",
            "Connaissance de l'organisation préfectorale",
            "Analyse de la menace",
            "Sécurité des grands rassemblements",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Conseiller(ère) transports et mobilités": {
        "mission": (
            "Préparer avec les autorités organisatrices le plan de transport "
            "des spectateurs, des délégations et des personnels."
        ),
        "profil_recherche": (
            "Expérience en planification des transports ou en exploitation de "
            "réseaux, connaissance des acteurs de la mobilité."
        ),
        "profil": [
            (
                "Ingénieur(e) transports, j'ai conçu des plans de mobilité pour "
                "des événements accueillant des centaines de milliers de visiteurs."
            ),
            (
                "Spécialiste de l'exploitation des réseaux, attaché(e) à la "
                "qualité de service pour les voyageurs."
            ),
        ],
        "formations": [
            _form("Master Transport et mobilité", "École d'urbanisme de Paris"),
            _form("Diplôme d'ingénieur, option transports", "INSA Lyon"),
            _form("Master Économie des transports", "Université Lumière Lyon 2"),
        ],
        "experiences_directes": [
            _exp(
                "Chef(fe) de projet mobilité événementielle",
                "Autorité organisatrice des mobilités régionale",
                "Conception des plans de transport et coordination des "
                "opérateurs ferroviaires et de bus.",
            ),
            _exp(
                "Responsable de l'offre de transport",
                "Opérateur de transport urbain",
                "Dimensionnement de l'offre, suivi de la fréquentation et "
                "gestion des situations perturbées.",
            ),
            _exp(
                "Chargé(e) d'études déplacements",
                "Bureau d'études en mobilité",
                "Modélisation des flux et élaboration de plans de déplacements "
                "pour des collectivités.",
            ),
            _exp(
                "Chargé(e) de mission voies olympiques",
                "Direction des routes d'Île-de-France",
                "Conception et exploitation de voies réservées, concertation "
                "avec les gestionnaires de voirie.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Planification des transports",
            "Modélisation des flux de voyageurs",
            "Exploitation de réseaux en situation perturbée",
            "Connaissance des autorités organisatrices",
            "Accessibilité des transports",
            "Gestion de la voirie et des voies réservées",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Chargé(e) de mission relations territoriales": {
        "mission": (
            "Animer le réseau des collectivités hôtes et des préfectures, "
            "relayer leurs attentes et suivre les engagements pris avec "
            "elles."
        ),
        "profil_recherche": (
            "Bonne connaissance des collectivités territoriales et de "
            "l'administration déconcentrée, aisance relationnelle."
        ),
        "profil": [
            (
                "Chargé(e) de relations avec les élus, j'ai animé des réseaux de "
                "collectivités autour de projets structurants."
            ),
            (
                "Spécialiste de l'action publique territoriale, habitué(e) au "
                "dialogue entre services de l'État et collectivités."
            ),
        ],
        "formations": [
            _form(
                "Master Administration des collectivités territoriales",
                "Université de Lille",
            ),
            _form("Master Affaires publiques", "Sciences Po Paris"),
            _form("Licence Administration publique", "Université de Rennes"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission relations avec les collectivités",
                "Préfecture de région",
                "Animation des contrats territoriaux et suivi des projets "
                "cofinancés par l'État.",
            ),
            _exp(
                "Responsable des relations institutionnelles",
                "Association d'élus locaux",
                "Représentation des collectivités et préparation des "
                "positions sur les textes en discussion.",
            ),
            _exp(
                "Chef(fe) de projet territorial",
                "Agence nationale de la cohésion des territoires",
                "Accompagnement de communes dans leurs programmes de revitalisation.",
            ),
            _exp(
                "Collaborateur(rice) de cabinet",
                "Conseil régional",
                "Suivi des relations avec les territoires et préparation des "
                "déplacements de l'exécutif.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Connaissance des collectivités territoriales",
            "Animation de réseaux d'acteurs locaux",
            "Relations avec les élus",
            "Contractualisation État-collectivités",
            "Organisation de concertations",
            "Suivi d'engagements partenariaux",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Chargé(e) de mission transition écologique et sobriété": {
        "mission": (
            "Porter les engagements environnementaux de la délégation : "
            "sobriété énergétique, réduction des déchets et bilan carbone "
            "des événements."
        ),
        "profil_recherche": (
            "Expérience en développement durable ou en transition "
            "énergétique, maîtrise des méthodes de bilan carbone."
        ),
        "profil": [
            (
                "Chargé(e) de mission développement durable, j'ai conduit des "
                "plans de sobriété et des bilans carbone d'événements."
            ),
            (
                "Ingénieur(e) environnement, convaincu(e) que la sobriété se "
                "construit avec les équipes opérationnelles."
            ),
        ],
        "formations": [
            _form("Master Transition écologique", "AgroParisTech"),
            _form("Diplôme d'ingénieur environnement", "Mines Paris"),
            _form(
                "Master Développement durable des organisations",
                "Université Paris-Dauphine",
            ),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission sobriété énergétique",
                "Ministère de la Transition écologique",
                "Animation du plan de sobriété des services et suivi des "
                "consommations.",
            ),
            _exp(
                "Responsable RSE",
                "Organisateur d'événements sportifs",
                "Réalisation de bilans carbone et pilotage des actions de "
                "réduction des déchets.",
            ),
            _exp(
                "Chef(fe) de projet climat-énergie",
                "Agence de la transition écologique",
                "Accompagnement de collectivités dans leurs plans climat.",
            ),
            _exp(
                "Consultant(e) carbone",
                "Cabinet spécialisé en transition énergétique",
                "Bilans d'émissions de gaz à effet de serre et trajectoires "
                "de réduction pour des acteurs publics.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Méthode Bilan Carbone",
            "Plans de sobriété énergétique",
            "Économie circulaire et réduction des déchets",
            "Achats publics responsables",
            "Animation de démarches RSE",
            "Réglementation environnementale",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "Chargé(e) de mission accessibilité et Jeux paralympiques": {
        "mission": (
            "Garantir l'accessibilité des sites, des transports et des "
            "services aux personnes en situation de handicap, en lien avec "
            "le mouvement paralympique."
        ),
        "profil_recherche": (
            "Expérience des politiques du handicap ou de l'accessibilité du "
            "cadre bâti, connaissance du mouvement paralympique appréciée."
        ),
        "profil": [
            (
                "Spécialiste de l'accessibilité, j'ai accompagné des maîtres "
                "d'ouvrage dans la mise en conformité de leurs équipements."
            ),
            (
                "Chargé(e) de mission handicap, engagé(e) auprès des "
                "associations et du mouvement paralympique."
            ),
        ],
        "formations": [
            _form("Master Handicap et société", "Université de Grenoble"),
            _form(
                "Diplôme d'architecte d'État",
                "École nationale supérieure d'architecture de Nantes",
            ),
            _form("Master Politiques sociales", "Université de Strasbourg"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission accessibilité",
                "Ville de Paris",
                "Diagnostic des établissements recevant du public et suivi des "
                "agendas d'accessibilité programmée.",
            ),
            _exp(
                "Référent(e) handicap",
                "Comité paralympique et sportif français",
                "Accompagnement des clubs dans l'accueil des pratiquants en "
                "situation de handicap.",
            ),
            _exp(
                "Conseiller(ère) accessibilité",
                "Bureau de contrôle technique",
                "Vérification de la conformité des projets de construction aux "
                "règles d'accessibilité.",
            ),
            _exp(
                "Chef(fe) de projet inclusion",
                "Maison départementale des personnes handicapées",
                "Pilotage de projets d'inclusion et animation des partenaires.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Réglementation de l'accessibilité du cadre bâti",
            "Connaissance du mouvement paralympique",
            "Diagnostic d'accessibilité",
            "Accessibilité des transports et de l'information",
            "Dialogue avec les associations de personnes handicapées",
            "Politiques publiques du handicap",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
}

VILLES = [
    "Paris",
    "Saint-Denis",
    "Lyon",
    "Marseille",
    "Lille",
    "Bordeaux",
    "Nantes",
    "Toulouse",
    "Strasbourg",
    "Rennes",
    "Montpellier",
    "Nice",
    "Grenoble",
    "Dijon",
    "Orléans",
    "Versailles",
    "Créteil",
    "Nanterre",
]

LANGUES = [
    "Anglais courant (C1), espagnol intermédiaire (B1)",
    "Anglais professionnel (B2), allemand notions",
    "Anglais courant (C1), italien intermédiaire (B2)",
    "Anglais intermédiaire (B2), langue des signes française notions",
]

NOTE_LIGNES = [
    "Candidat(e) : {prenom} {nom}, poste de {intitule}.",
    "Entretien de présélection téléphonique d'une trentaine de minutes.",
    "Dernière expérience : {experience}.",
    "{appreciation}",
    "Point fort relevé : {competence}.",
    "Motivation claire pour l'organisation des Jeux et le service public.",
    "Bonne capacité à présenter ses réalisations de façon structurée.",
    "Compréhension correcte des enjeux du poste et de son environnement.",
    "Point de vigilance : expérience de l'interministériel à approfondir.",
    "Disponibilité annoncée sous un mois, mobilité géographique possible.",
    "Prétentions salariales compatibles avec la grille du poste.",
    "Références professionnelles proposées, à contacter si poursuite.",
    "Aisance à l'oral, propos précis et adaptés à l'interlocuteur.",
    "Avis : favorable à un entretien avec le responsable du recrutement.",
    "Prochaine étape : proposer trois créneaux d'entretien.",
]
