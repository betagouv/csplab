from typing import Literal, TypedDict


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


Famille = Literal[
    "pilotage",
    "rh",
    "juridique",
    "finances",
    "achats",
    "numerique",
    "communication",
    "culture",
    "audit",
    "environnement",
    "solidarites",
]


class Corpus(TypedDict):
    pilotage: PosteCorpus
    rh: PosteCorpus
    juridique: PosteCorpus
    finances: PosteCorpus
    achats: PosteCorpus
    numerique: PosteCorpus
    communication: PosteCorpus
    culture: PosteCorpus
    audit: PosteCorpus
    environnement: PosteCorpus
    solidarites: PosteCorpus


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

CORPUS: Corpus = {
    "pilotage": {
        "mission": (
            "Appuyer la direction dans le pilotage de ses activités : "
            "coordination des services, préparation des arbitrages, suivi des "
            "projets transverses et des fonctions support."
        ),
        "profil_recherche": (
            "Expérience de l'appui à une direction ou de la coordination de "
            "projets, sens de l'organisation et qualités rédactionnelles."
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
                "Directeur(trice) des ressources humaines",
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
    "rh": {
        "mission": (
            "Accompagner les agents et les services sur l'ensemble des sujets "
            "de ressources humaines : carrière, paie, recrutement, formation "
            "et dialogue social."
        ),
        "profil_recherche": (
            "Expérience de la gestion des ressources humaines dans le secteur "
            "public, bonne connaissance du statut général."
        ),
        "profil": [
            (
                "Gestionnaire RH depuis sept ans, j'ai suivi la carrière et la "
                "paie de plusieurs centaines d'agents."
            ),
            (
                "Conseiller(ère) en ressources humaines, attaché(e) à "
                "l'accompagnement des parcours et au dialogue social."
            ),
        ],
        "formations": [
            _form("Master Gestion des ressources humaines", "IAE de Paris"),
            _form(
                "Master Droit et gestion de la fonction publique",
                "Université de Bordeaux",
            ),
            _form(
                "Licence Administration économique et sociale", "Université de Nantes"
            ),
        ],
        "experiences_directes": [
            _exp(
                "Gestionnaire carrière et paie",
                "Centre de gestion de la fonction publique territoriale",
                "Suivi des avancements, des positions statutaires et de la "
                "paie pour environ 300 agents.",
            ),
            _exp(
                "Chargé(e) de recrutement",
                "Direction des ressources humaines d'un ministère",
                "Rédaction des fiches de poste, conduite des entretiens et "
                "animation des commissions de sélection.",
            ),
            _exp(
                "Conseiller(ère) mobilité carrière",
                "Plateforme régionale d'appui interministériel à la GRH",
                "Accompagnement individuel des agents dans leurs projets de "
                "mobilité et de reconversion.",
            ),
            _exp(
                "Responsable formation",
                "Établissement public hospitalier",
                "Élaboration du plan de formation, suivi des budgets et "
                "évaluation des actions.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Statut général de la fonction publique",
            "Gestion de la paie et des carrières",
            "Conduite d'entretiens de recrutement",
            "Ingénierie de formation",
            "Dialogue social et instances représentatives",
            "Maîtrise d'un SIRH",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "juridique": {
        "mission": (
            "Sécuriser juridiquement les décisions de la direction, suivre "
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
                "Administrateur(trice) adjoint(e)",
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
    "finances": {
        "mission": (
            "Suivre les engagements financiers de l’État, préparer les "
            "arbitrages budgétaires et analyser la situation économique et "
            "financière des secteurs suivis."
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
                "Économiste",
                "Institut national de la statistique et des études économiques",
                "Analyse conjoncturelle, prévisions macroéconomiques et "
                "rédaction de notes de conjoncture.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Finances publiques et LOLF",
            "Analyse des risques financiers",
            "Préparation des lois de finances",
            "Analyse économique et conjoncturelle",
            "Contrôle de gestion",
            "Modélisation financière sous tableur",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "achats": {
        "mission": (
            "Définir les stratégies d'achat, conduire les procédures de "
            "marchés publics et suivre leur exécution avec les services "
            "prescripteurs."
        ),
        "profil_recherche": (
            "Expérience de la commande publique, maîtrise du code et des "
            "procédures, sens de la négociation."
        ),
        "profil": [
            (
                "Acheteur(se) public(que) depuis cinq ans, j'ai conduit des "
                "procédures formalisées de travaux, fournitures et services."
            ),
            (
                "Spécialiste de la commande publique, attaché(e) à l'achat "
                "responsable et à la performance économique."
            ),
        ],
        "formations": [
            _form("Master Achats publics", "Université de Lille"),
            _form("Master Droit des contrats publics", "Université Jean Moulin Lyon 3"),
            _form("Licence professionnelle Achats", "IUT de Bordeaux"),
        ],
        "experiences_directes": [
            _exp(
                "Acheteur(se) public(que)",
                "Direction des achats de l'État",
                "Passation de marchés interministériels, analyse des offres et "
                "négociation avec les fournisseurs.",
            ),
            _exp(
                "Responsable de la commande publique",
                "Conseil départemental",
                "Programmation des achats, sécurisation des procédures et "
                "suivi de l'exécution financière.",
            ),
            _exp(
                "Chargé(e) des marchés de travaux",
                "Établissement public d'aménagement",
                "Rédaction des dossiers de consultation et gestion des "
                "avenants et des réclamations.",
            ),
            _exp(
                "Juriste marchés publics",
                "Union des groupements d'achats publics",
                "Conseil aux acheteurs publics et rédaction de clauses "
                "environnementales et sociales.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Code de la commande publique",
            "Rédaction de cahiers des charges",
            "Analyse des offres et négociation",
            "Achat public responsable",
            "Suivi de l'exécution des marchés",
            "Maîtrise des plateformes de dématérialisation",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "numerique": {
        "mission": (
            "Concevoir, faire évoluer et sécuriser les services numériques et "
            "les systèmes d'information au service des agents et des usagers."
        ),
        "profil_recherche": (
            "Formation en informatique, expérience du développement, de la "
            "gestion de produit ou de l'exploitation de systèmes."
        ),
        "profil": [
            (
                "Développeur(se) depuis six ans, j'ai construit des services "
                "numériques publics utilisés par des millions d'usagers."
            ),
            (
                "Chef(fe) de projet SI, à l'aise entre les équipes techniques, "
                "les métiers et les prestataires."
            ),
        ],
        "formations": [
            _form("Diplôme d'ingénieur informatique", "INSA Rennes"),
            _form("Master Science des données", "Université Paris Cité"),
            _form(
                "Master Sécurité des systèmes d'information", "Université de Limoges"
            ),
        ],
        "experiences_directes": [
            _exp(
                "Développeur(se) full stack",
                "Direction interministérielle du numérique",
                "Développement d'une application web en Python et Vue, mise "
                "en production et suivi de l'usage.",
            ),
            _exp(
                "Chef(fe) de projet systèmes d'information",
                "Ministère de l'Économie et des Finances",
                "Pilotage de la refonte d'un applicatif métier, recette et "
                "accompagnement des utilisateurs.",
            ),
            _exp(
                "Data analyst",
                "Agence régionale de santé",
                "Construction de tableaux de bord et automatisation des "
                "traitements de données.",
            ),
            _exp(
                "Ingénieur(e) sécurité des systèmes d'information",
                "Opérateur d'importance vitale",
                "Analyses de risques, homologation des systèmes et réponse "
                "aux incidents de sécurité.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Développement web (Python, JavaScript)",
            "Méthodes agiles et gestion de produit",
            "Analyse et visualisation de données",
            "Sécurité des systèmes d'information",
            "Administration de bases de données",
            "Accessibilité numérique (RGAA)",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "communication": {
        "mission": (
            "Concevoir et mettre en œuvre la communication interne et "
            "externe, animer les réseaux sociaux et gérer les relations avec "
            "la presse."
        ),
        "profil_recherche": (
            "Expérience de la communication publique, excellentes qualités "
            "rédactionnelles et maîtrise des outils numériques."
        ),
        "profil": [
            (
                "Chargé(e) de communication depuis six ans, j'ai conduit des "
                "campagnes d'information du public pour des acteurs publics."
            ),
            (
                "Spécialiste des réseaux sociaux et des relations presse, "
                "attaché(e) à une information claire et accessible."
            ),
        ],
        "formations": [
            _form("Master Communication publique et politique", "CELSA Sorbonne"),
            _form("Diplôme de journalisme", "École supérieure de journalisme de Lille"),
            _form("Master Communication des organisations", "Université de Toulouse"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de communication digitale",
                "Service d'information du Gouvernement",
                "Animation des réseaux sociaux, production de contenus et "
                "suivi des indicateurs d'audience.",
            ),
            _exp(
                "Attaché(e) de presse",
                "Cabinet ministériel",
                "Rédaction de communiqués, organisation de conférences de "
                "presse et gestion des sollicitations.",
            ),
            _exp(
                "Responsable de la communication interne",
                "Établissement public national",
                "Conception de la lettre interne, animation de l'intranet et "
                "accompagnement des projets de transformation.",
            ),
            _exp(
                "Chargé(e) de mécénat et partenariats",
                "Musée national",
                "Prospection d'entreprises mécènes et suivi des contreparties.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Stratégie de communication publique",
            "Rédaction web et éditoriale",
            "Animation de réseaux sociaux",
            "Relations presse",
            "Communication de crise",
            "Création graphique et outils PAO",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "culture": {
        "mission": (
            "Contribuer à la conservation, à la valorisation et à la "
            "diffusion du patrimoine et de la création, en lien avec les "
            "institutions culturelles et les publics."
        ),
        "profil_recherche": (
            "Formation en histoire de l'art, patrimoine ou médiation, "
            "expérience d'une institution culturelle."
        ),
        "profil": [
            (
                "Historien(ne) de l'art, j'ai participé à l'organisation "
                "d'expositions et à la gestion de collections publiques."
            ),
            (
                "Médiateur(trice) culturel(le), attaché(e) à l'ouverture des "
                "institutions à tous les publics."
            ),
        ],
        "formations": [
            _form("Diplôme de l'École du Louvre", "École du Louvre"),
            _form("Master Histoire de l'art", "Université Paris 1 Panthéon-Sorbonne"),
            _form("Master Médiation culturelle", "Université Sorbonne Nouvelle"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de production d'expositions",
                "Musée d'art moderne",
                "Coordination des prêts, des transports d'œuvres et du "
                "calendrier de montage.",
            ),
            _exp(
                "Régisseur(se) des collections",
                "Musée départemental",
                "Inventaire, récolement et conditionnement des œuvres, suivi "
                "des mouvements.",
            ),
            _exp(
                "Chargé(e) des publics",
                "Centre d'art contemporain",
                "Conception des visites et ateliers, partenariats avec les "
                "établissements scolaires.",
            ),
            _exp(
                "Conseiller(ère) pour les patrimoines",
                "Direction régionale des affaires culturelles",
                "Instruction des demandes de protection et suivi des "
                "chantiers sur monuments historiques.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Gestion et conservation de collections",
            "Organisation d'expositions",
            "Médiation et éducation artistique",
            "Droit du patrimoine",
            "Régie et conditionnement d'œuvres",
            "Montage de projets culturels",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "audit": {
        "mission": (
            "Contrôler la régularité et la qualité de la gestion publique, "
            "évaluer les politiques publiques et formuler des recommandations."
        ),
        "profil_recherche": (
            "Expérience de l'audit, du contrôle ou de l'évaluation, rigueur "
            "méthodologique et qualités rédactionnelles."
        ),
        "profil": [
            (
                "Auditeur(trice) depuis huit ans, j'ai conduit des missions de "
                "contrôle auprès d'organismes publics."
            ),
            (
                "Chargé(e) d'évaluation, attaché(e) à éclairer la décision "
                "publique par des analyses étayées."
            ),
        ],
        "formations": [
            _form("Master Audit et contrôle", "Université Paris-Dauphine"),
            _form("Master Évaluation des politiques publiques", "Sciences Po Lyon"),
            _form("Diplôme d'expertise comptable", "Ordre des experts-comptables"),
        ],
        "experiences_directes": [
            _exp(
                "Vérificateur(trice)",
                "Chambre régionale des comptes",
                "Contrôle des comptes et de la gestion de collectivités, "
                "rédaction de rapports d'observations.",
            ),
            _exp(
                "Auditeur(trice) interne",
                "Ministère des Armées",
                "Audits de processus, cartographie des risques et suivi des "
                "plans d'action.",
            ),
            _exp(
                "Chargé(e) d'évaluation",
                "France Stratégie",
                "Évaluation d'impact de dispositifs publics et rédaction de rapports.",
            ),
            _exp(
                "Auditeur(trice) financier(ère)",
                "Cabinet d'audit",
                "Certification des comptes d'établissements publics et d'associations.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Méthodologie d'audit et de contrôle",
            "Analyse financière et comptabilité publique",
            "Évaluation des politiques publiques",
            "Cartographie des risques",
            "Rédaction de rapports et de recommandations",
            "Procédure contradictoire",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "environnement": {
        "mission": (
            "Concevoir et suivre des politiques de transition écologique : "
            "climat, biodiversité, prévention des risques, mobilités et "
            "aménagement durable des territoires."
        ),
        "profil_recherche": (
            "Expérience en environnement, en aménagement ou en mobilité, "
            "connaissance des collectivités et des services de l'État."
        ),
        "profil": [
            (
                "Chargé(e) de mission développement durable, j'ai conduit des "
                "plans de sobriété et des démarches climat-énergie."
            ),
            (
                "Ingénieur(e) environnement, habitué(e) au dialogue entre "
                "services de l'État, collectivités et acteurs locaux."
            ),
        ],
        "formations": [
            _form("Master Transition écologique", "AgroParisTech"),
            _form("Diplôme d'ingénieur environnement", "Mines Paris"),
            _form("Master Transport et mobilité", "École d'urbanisme de Paris"),
        ],
        "experiences_directes": [
            _exp(
                "Chargé(e) de mission sobriété énergétique",
                "Ministère de la Transition écologique",
                "Animation du plan de sobriété des services et suivi des "
                "consommations.",
            ),
            _exp(
                "Chef(fe) de projet climat-énergie",
                "Agence de la transition écologique",
                "Accompagnement de collectivités dans leurs plans climat.",
            ),
            _exp(
                "Chef(fe) de projet territorial",
                "Agence nationale de la cohésion des territoires",
                "Accompagnement de communes dans leurs programmes de revitalisation.",
            ),
            _exp(
                "Chargé(e) d'études mobilité",
                "Autorité organisatrice des mobilités régionale",
                "Conception de plans de mobilité et coordination des "
                "opérateurs ferroviaires et de bus.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Méthode Bilan Carbone",
            "Plans de sobriété énergétique",
            "Économie circulaire et réduction des déchets",
            "Réglementation environnementale",
            "Planification des transports",
            "Contractualisation État-collectivités",
        ],
        "competences_voisines": _COMPETENCES_TRANSVERSES,
    },
    "solidarites": {
        "mission": (
            "Concevoir et suivre les politiques du travail, de l'emploi et des "
            "solidarités, en lien avec les services déconcentrés et les "
            "partenaires sociaux."
        ),
        "profil_recherche": (
            "Expérience des politiques sociales ou de l'emploi, connaissance "
            "du droit du travail et des acteurs de l'insertion."
        ),
        "profil": [
            (
                "Chargé(e) de mission insertion depuis six ans, j'ai animé des "
                "dispositifs d'accompagnement vers l'emploi."
            ),
            (
                "Spécialiste des politiques sociales, attaché(e) à l'accès aux "
                "droits et à la lutte contre la pauvreté."
            ),
        ],
        "formations": [
            _form("Master Politiques sociales", "Université de Strasbourg"),
            _form("Master Droit social", "Université Paris Nanterre"),
            _form("Master Économie du travail", "Université Lumière Lyon 2"),
        ],
        "experiences_directes": [
            _exp(
                "Inspecteur(trice) du travail",
                "Direction régionale de l'économie, de l'emploi, du travail "
                "et des solidarités",
                "Contrôle de l'application du droit du travail et conseil aux "
                "entreprises et aux salariés.",
            ),
            _exp(
                "Chargé(e) de mission insertion",
                "Conseil départemental",
                "Pilotage du programme départemental d'insertion et suivi des "
                "structures d'insertion par l'activité économique.",
            ),
            _exp(
                "Chargé(e) d'études statistiques",
                "Direction de l'animation de la recherche, des études et des "
                "statistiques",
                "Production d'indicateurs sur l'emploi et analyses des "
                "dispositifs de politique de l'emploi.",
            ),
            _exp(
                "Chef(fe) de projet autonomie",
                "Caisse nationale de solidarité pour l'autonomie",
                "Suivi des plans d'aide aux personnes âgées et handicapées et "
                "animation des départements.",
            ),
        ],
        "experiences_voisines": _EXPERIENCES_TRANSVERSES,
        "competences_poste": [
            "Droit du travail",
            "Politiques de l'emploi et de l'insertion",
            "Politiques de l'autonomie et du handicap",
            "Analyse statistique de l'emploi",
            "Animation de partenariats institutionnels",
            "Dialogue avec les partenaires sociaux",
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
