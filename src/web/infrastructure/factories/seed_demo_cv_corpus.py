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
    _exp(
        "Chargé(e) de mission",
        "Communauté urbaine de Dunkerque",
        "Suivi de projets transversaux et préparation des conseils communautaires.",
    ),
    _exp(
        "Gestionnaire administratif(ve)",
        "Ville de Nantes",
        "Instruction de dossiers, accueil des usagers et suivi budgétaire "
        "d'un service municipal.",
    ),
    _exp(
        "Chargé(e) d'études",
        "Caisse des dépôts et consignations",
        "Études territoriales et appui aux collectivités dans leurs projets "
        "d'investissement.",
    ),
    _exp(
        "Responsable administratif(ve)",
        "Université de Lille",
        "Pilotage d'un service administratif et gestion des moyens d'une composante.",
    ),
]

_COMPETENCES_TRANSVERSES = [
    "Conduite de projet et animation d'équipes pluridisciplinaires",
    "Rédaction de notes de synthèse et d'éléments de langage",
    "Préparation et animation de comités de pilotage",
    "Maîtrise des outils bureautiques et collaboratifs",
    "Sens du service public et devoir de réserve",
    "Capacité d'analyse et esprit de synthèse",
    "Gestion des priorités et respect des délais",
    "Aisance à l'oral et prise de parole en public",
    "Accueil et relation avec les usagers",
    "Travail en réseau et en partenariat",
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
            (
                "Assistant(e) de direction expérimenté(e), je coordonne depuis "
                "cinq ans l'agenda et les dossiers d'un comité de direction."
            ),
            (
                "Chef(fe) de projet transformation, j'ai mené plusieurs chantiers "
                "de simplification des démarches internes."
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
            _form("Master Management public", "Université de Strasbourg"),
            _form(
                "Classe préparatoire aux concours administratifs",
                "Institut régional d'administration de Lille",
            ),
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
            _exp(
                "Chargé(e) de mission auprès du directeur",
                "Direction départementale des territoires de l'Isère",
                "Préparation des comités de direction, suivi des tableaux de "
                "bord et coordination des chefs de service.",
            ),
            _exp(
                "Assistant(e) de direction",
                "Rectorat de l'académie de Versailles",
                "Gestion de l'agenda, organisation des réunions et suivi du "
                "courrier du recteur.",
            ),
            _exp(
                "Chef(fe) de projet transformation",
                "Direction interministérielle de la transformation publique",
                "Conduite de projets de simplification et animation de réseaux "
                "de porteurs de projets.",
            ),
            _exp(
                "Responsable des services généraux",
                "Office national des forêts",
                "Gestion des bâtiments, de la flotte automobile et des contrats "
                "de maintenance.",
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
            "Préparation des arbitrages de la direction",
            "Organisation logistique de déplacements et d'événements",
            "Suivi de tableaux de bord et d'indicateurs",
            "Conduite du changement",
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
            (
                "Gestionnaire paie rigoureux(se), habitué(e) aux contrôles de fin "
                "d'exercice et aux évolutions réglementaires."
            ),
            (
                "Chargé(e) de recrutement, je conduis chaque année plus de deux "
                "cents entretiens pour des postes très variés."
            ),
        ],
        "formations": [
            _form("Master Gestion des ressources humaines", "IAE de Paris"),
            _form(
                "Master Droit et gestion de la fonction publique",
                "Université de Bordeaux",
            ),
            _form(
                "Licence Administration économique et sociale",
                "Université de Nantes",
            ),
            _form(
                "Master Ressources humaines et relations du travail",
                "Université de Montpellier",
            ),
            _form("Licence professionnelle Gestion de la paie", "IUT de Tours"),
            _form("Master Psychologie du travail", "Université de Lorraine"),
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
            _exp(
                "Gestionnaire paie",
                "Centre hospitalier universitaire de Rennes",
                "Préparation et contrôle de la paie mensuelle, gestion des "
                "absences et des cotisations.",
            ),
            _exp(
                "Chargé(e) de mission égalité professionnelle",
                "Région Auvergne-Rhône-Alpes",
                "Pilotage du plan d'action égalité, suivi des indicateurs et "
                "animation du réseau de référents.",
            ),
            _exp(
                "Conseiller(ère) en prévention",
                "Service départemental d'incendie et de secours",
                "Analyse des risques professionnels, mise à jour du document "
                "unique et accompagnement des encadrants.",
            ),
            _exp(
                "Responsable du dialogue social",
                "Météo-France",
                "Préparation des instances, rédaction des procès-verbaux et "
                "suivi des accords.",
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
            "Gestion prévisionnelle des emplois et des compétences",
            "Prévention des risques professionnels",
            "Accompagnement des mobilités",
            "Politique d'égalité professionnelle",
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
            (
                "Ancien(ne) avocat(e), j'ai plaidé en contentieux administratif "
                "avant de rejoindre une administration."
            ),
            (
                "Juriste spécialisé(e) en droit économique, à l'aise avec "
                "l'analyse de marchés et de contrats."
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
            _form("Master Droit de l'environnement", "Université de Strasbourg"),
            _form("Master Propriété intellectuelle", "Université de Poitiers"),
            _form("Diplôme de Sciences Po", "Sciences Po Grenoble"),
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
            _exp(
                "Juriste",
                "Agence de l'eau Seine-Normandie",
                "Instruction juridique des aides et sécurisation des actes de "
                "l'agence.",
            ),
            _exp(
                "Juriste propriété intellectuelle",
                "Institut national de la propriété industrielle",
                "Conseil sur le droit des marques et des brevets et rédaction de "
                "contrats de licence.",
            ),
            _exp(
                "Avocat(e) collaborateur(trice)",
                "Cabinet d'avocats en droit public",
                "Contentieux des contrats publics et de la fonction publique.",
            ),
            _exp(
                "Rapporteur(e)",
                "Autorité de la concurrence",
                "Instruction de dossiers de concentration et rédaction de "
                "projets de décision.",
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
            "Droit de la propriété intellectuelle",
            "Droit de la concurrence",
            "Droit de l'environnement",
            "Rédaction de contrats et de conventions",
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
            (
                "Économiste, je produis depuis six ans des analyses "
                "conjoncturelles et sectorielles pour l’État."
            ),
            (
                "Contrôleur(se) de gestion, soucieux(se) de la fiabilité des données "
                "et du dialogue de gestion avec les services de l’État."
            ),
        ],
        "formations": [
            _form("Master Finances publiques", "Université Paris 1 Panthéon-Sorbonne"),
            _form("Master Contrôle de gestion et audit", "IAE d'Aix-Marseille"),
            _form("Diplôme de l'ESSEC, majeure finance", "ESSEC Business School"),
            _form("Master Économie appliquée", "Toulouse School of Economics"),
            _form("Diplôme d'ingénieur statisticien économiste", "ENSAE Paris"),
            _form("Master Banque et finance", "Université de Lille"),
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
            _exp(
                "Inspecteur(trice) des finances publiques",
                "Direction générale des finances publiques",
                "Contrôle fiscal des entreprises et analyse de leurs comptes.",
            ),
            _exp(
                "Analyste financier(ère)",
                "Bpifrance",
                "Analyse de dossiers de financement et suivi d'un portefeuille "
                "d'entreprises.",
            ),
            _exp(
                "Responsable budgétaire",
                "Université de Bordeaux",
                "Préparation du budget, dialogue de gestion avec les "
                "composantes et suivi de l'exécution.",
            ),
            _exp(
                "Chargé(e) de mission participations",
                "Agence des participations de l'État",
                "Suivi d'entreprises du portefeuille public et préparation des "
                "conseils d'administration.",
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
            "Fiscalité des entreprises",
            "Analyse de bilans et de comptes",
            "Prévision macroéconomique",
            "Suivi de la performance des opérateurs",
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
            (
                "Acheteur(se) informatique, habitué(e) aux marchés complexes et à "
                "la négociation avec les éditeurs."
            ),
            (
                "Ancien(ne) juriste, je sécurise les procédures de passation et "
                "l'exécution des marchés."
            ),
        ],
        "formations": [
            _form("Master Achats publics", "Université de Lille"),
            _form("Master Droit des contrats publics", "Université Jean Moulin Lyon 3"),
            _form("Licence professionnelle Achats", "IUT de Bordeaux"),
            _form("Master Management des achats", "IAE de Grenoble"),
            _form("Master Droit public des affaires", "Université de Rennes"),
            _form("Licence Administration publique", "Université de Nantes"),
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
            _exp(
                "Acheteur(se) informatique",
                "Centre hospitalier régional universitaire de Lille",
                "Achats de matériels et de prestations informatiques, mise en "
                "concurrence et suivi des fournisseurs.",
            ),
            _exp(
                "Responsable des achats",
                "Ville de Toulouse",
                "Animation de la fonction achat et élaboration de la "
                "cartographie des achats.",
            ),
            _exp(
                "Chargé(e) de l'exécution des marchés",
                "Voies navigables de France",
                "Suivi financier des marchés, gestion des pénalités et des "
                "reconductions.",
            ),
            _exp(
                "Acheteur(se) prestations intellectuelles",
                "Ministère des Armées, plateforme achats",
                "Passation de marchés d'études et de conseil, analyse des offres.",
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
            "Sourcing et connaissance des marchés fournisseurs",
            "Cartographie des achats",
            "Gestion des avenants et des reconductions",
            "Suivi de la relation fournisseurs",
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
            (
                "Data scientist, j'aime transformer des données publiques en "
                "outils utiles aux agents."
            ),
            (
                "Administrateur(trice) systèmes, j'assure depuis cinq ans "
                "l'exploitation de services critiques."
            ),
        ],
        "formations": [
            _form("Diplôme d'ingénieur informatique", "INSA Rennes"),
            _form("Master Science des données", "Université Paris Cité"),
            _form(
                "Master Sécurité des systèmes d'information",
                "Université de Limoges",
            ),
            _form(
                "Licence professionnelle Administration de systèmes",
                "IUT de Lannion",
            ),
            _form("Master MIAGE", "Université Paris-Dauphine"),
            _form("Diplôme d'ingénieur", "EPITA"),
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
            _exp(
                "Administrateur(trice) systèmes et réseaux",
                "Université Grenoble Alpes",
                "Exploitation de serveurs Linux, supervision et sauvegardes.",
            ),
            _exp(
                "Chef(fe) de produit numérique",
                "Incubateur de services numériques de l'État",
                "Pilotage d'un produit par l'usage, priorisation et suivi des "
                "indicateurs d'impact.",
            ),
            _exp(
                "Data scientist",
                "Caisse nationale de l'assurance maladie",
                "Modèles statistiques de détection des fraudes et visualisation "
                "de données de santé.",
            ),
            _exp(
                "Développeur(se) back-end",
                "Entreprise de services numériques",
                "Développement d'API et maintenance d'applications pour des "
                "clients publics.",
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
            "Administration de systèmes Linux",
            "Conception d'API",
            "Recherche utilisateur et tests d'usage",
            "Modélisation statistique et apprentissage automatique",
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
            (
                "Rédacteur(trice) web, je conçois depuis quatre ans des contenus "
                "pour des sites institutionnels."
            ),
            (
                "Chargé(e) de veille, habitué(e) à repérer les signaux faibles "
                "dans les médias et sur les réseaux."
            ),
        ],
        "formations": [
            _form("Master Communication publique et politique", "CELSA Sorbonne"),
            _form(
                "Diplôme de journalisme",
                "École supérieure de journalisme de Lille",
            ),
            _form(
                "Master Communication des organisations",
                "Université de Toulouse",
            ),
            _form(
                "Licence Information-communication",
                "Université Bordeaux Montaigne",
            ),
            _form("Master Communication numérique", "Université de Lorraine"),
            _form(
                "Master Médias et communication", "Université Paris 2 Panthéon-Assas"
            ),
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
            _exp(
                "Chargé(e) de communication éditoriale",
                "Bibliothèque nationale de France",
                "Rédaction de contenus pour le site et les réseaux, "
                "coordination des publications.",
            ),
            _exp(
                "Responsable de la communication",
                "Communauté de communes du Pays de Gex",
                "Conception des campagnes locales et gestion du magazine "
                "intercommunal.",
            ),
            _exp(
                "Chargé(e) de relations presse",
                "Agence de communication publique",
                "Gestion de fichiers presse et organisation de voyages de "
                "presse pour des institutions.",
            ),
            _exp(
                "Chargé(e) de veille médias",
                "Préfecture de police",
                "Revue de presse quotidienne et analyse des réseaux sociaux.",
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
            "Veille médias et réseaux sociaux",
            "Gestion de site web et de CMS",
            "Organisation d'événements",
            "Communication accessible (FALC)",
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
            (
                "Archiviste, j'ai mené des opérations de classement "
                "et de valorisation de fonds publics."
            ),
            (
                "Chargé(e) de programmation, je construis des saisons qui relient "
                "artistes, territoires et publics."
            ),
        ],
        "formations": [
            _form("Diplôme de l'École du Louvre", "École du Louvre"),
            _form("Master Histoire de l'art", "Université Paris 1 Panthéon-Sorbonne"),
            _form("Master Médiation culturelle", "Université Sorbonne Nouvelle"),
            _form("Master Archives", "École nationale des chartes"),
            _form("Master Archéologie", "Université Toulouse - Jean Jaurès"),
            _form(
                "Diplôme de conservateur du patrimoine",
                "Institut national du patrimoine",
            ),
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
            _exp(
                "Archiviste",
                "Archives départementales du Rhône",
                "Classement de fonds, rédaction d'inventaires et accueil des lecteurs.",
            ),
            _exp(
                "Chargé(e) de programmation",
                "Scène nationale",
                "Programmation, accueil des compagnies et développement des publics.",
            ),
            _exp(
                "Bibliothécaire",
                "Médiathèque intercommunale",
                "Politique documentaire, animations autour du livre et "
                "partenariats scolaires.",
            ),
            _exp(
                "Chargé(e) d'études archéologiques",
                "Institut national de recherches archéologiques préventives",
                "Diagnostics de terrain, études de mobilier et rédaction de rapports.",
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
            "Classement et description d'archives",
            "Programmation artistique",
            "Politique documentaire",
            "Archéologie préventive",
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
            (
                "Ancien(ne) inspecteur(trice), rompu(e) aux missions "
                "d'évaluation interministérielles."
            ),
            (
                "Contrôleur(se) interne, j'ai déployé des plans de contrôle dans "
                "deux agences publiques."
            ),
        ],
        "formations": [
            _form("Master Audit et contrôle", "Université Paris-Dauphine"),
            _form("Master Évaluation des politiques publiques", "Sciences Po Lyon"),
            _form("Diplôme d'expertise comptable", "Ordre des experts-comptables"),
            _form("Master Comptabilité, contrôle, audit", "IAE de Bordeaux"),
            _form("Master Politiques publiques", "Sciences Po Paris"),
            _form(
                "Diplôme supérieur de comptabilité et de gestion",
                "Institut national des techniques économiques et comptables",
            ),
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
            _exp(
                "Inspecteur(trice)",
                "Inspection générale de l'administration",
                "Missions d'inspection et d'évaluation, rédaction de rapports "
                "au ministre.",
            ),
            _exp(
                "Contrôleur(se) interne comptable",
                "Agence de services et de paiement",
                "Cartographie des risques comptables et plans de contrôle.",
            ),
            _exp(
                "Auditeur(trice) des fonds européens",
                "Commission interministérielle de coordination des contrôles",
                "Audits d'opérations cofinancées et suivi des recommandations.",
            ),
            _exp(
                "Auditeur(trice) des systèmes d'information",
                "Société de conseil en cybersécurité",
                "Revue des contrôles généraux informatiques et des habilitations.",
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
            "Contrôle interne comptable",
            "Audit des fonds européens",
            "Audit des systèmes d'information",
            "Conduite d'entretiens d'audit",
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
            (
                "Écologue, j'accompagne depuis sept ans des projets "
                "de protection de la biodiversité."
            ),
            (
                "Inspecteur(trice) de l'environnement, j'ai contrôlé une "
                "centaine de sites industriels."
            ),
        ],
        "formations": [
            _form("Master Transition écologique", "AgroParisTech"),
            _form("Diplôme d'ingénieur environnement", "Mines Paris"),
            _form("Master Transport et mobilité", "École d'urbanisme de Paris"),
            _form("Master Écologie et biodiversité", "Université de Montpellier"),
            _form("Master Gestion des risques", "Université Grenoble Alpes"),
            _form("Diplôme d'ingénieur des travaux publics de l'État", "ENTPE"),
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
            _exp(
                "Inspecteur(trice) des installations classées",
                "Unité départementale de la DREAL des Hauts-de-France",
                "Inspection de sites industriels et instruction des dossiers "
                "d'autorisation.",
            ),
            _exp(
                "Chargé(e) de mission biodiversité",
                "Office français de la biodiversité",
                "Animation de plans d'action pour les espèces protégées et "
                "suivi des aires protégées.",
            ),
            _exp(
                "Chargé(e) d'études risques naturels",
                "Bureau de recherches géologiques et minières",
                "Cartographie des aléas et appui aux plans de prévention.",
            ),
            _exp(
                "Chargé(e) de mission économie circulaire",
                "Métropole Rouen Normandie",
                "Plan de réduction des déchets et accompagnement des "
                "entreprises du territoire.",
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
            "Inspection des installations classées",
            "Gestion des espaces naturels protégés",
            "Prévention des risques naturels",
            "Évaluation environnementale des projets",
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
            (
                "Conseiller(ère) en insertion, j'accompagne depuis huit ans des "
                "publics éloignés de l'emploi."
            ),
            (
                "Statisticien(ne) de l'emploi, je produis des indicateurs pour "
                "éclairer les politiques publiques."
            ),
        ],
        "formations": [
            _form("Master Politiques sociales", "Université de Strasbourg"),
            _form("Master Droit social", "Université Paris Nanterre"),
            _form("Master Économie du travail", "Université Lumière Lyon 2"),
            _form(
                "Diplôme d'État d'assistant de service social",
                "Institut régional du travail social d'Île-de-France",
            ),
            _form("Master Statistique et économétrie", "Université de Rennes"),
            _form("Master Sociologie", "Université de Nantes"),
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
            _exp(
                "Conseiller(ère) en insertion professionnelle",
                "France Travail",
                "Accompagnement de demandeurs d'emploi et relation avec les "
                "entreprises.",
            ),
            _exp(
                "Chargé(e) de mission handicap",
                "Association de gestion du fonds pour l'insertion des personnes "
                "handicapées",
                "Accompagnement des employeurs dans l'emploi des travailleurs "
                "handicapés.",
            ),
            _exp(
                "Contrôleur(se) du travail",
                "Unité départementale de l'inspection du travail",
                "Enquêtes en entreprise et suivi des accidents du travail.",
            ),
            _exp(
                "Chargé(e) de mission accès aux droits",
                "Union nationale des centres communaux d'action sociale",
                "Animation du réseau et appui aux projets d'accès aux droits.",
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
            "Accompagnement vers l'emploi",
            "Accès aux droits sociaux",
            "Emploi des personnes handicapées",
            "Enquêtes et contrôles en entreprise",
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
