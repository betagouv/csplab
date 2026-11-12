// Modèle et données de la variante « ATS — fiches et offres », aligné sur le cadrage « Offres ».
// Trois objets : la fiche de poste (référentiel), l'offre (informations internes, annonce, publication)
// et son formulaire de candidature. Tout est local et fictif ; conservé pendant la session (sessionStorage).

import { reactive } from 'vue'

export type OrigineFiche = 'ats' | 'sirh' | 'document'
/** Statut de l'offre. La validation n'est pas un statut : elle se suit à part (voir EtatValidation). */
export type EtatOffre = 'brouillon' | 'publiee' | 'retiree' | 'archivee'
export type EtatValidation = 'non_demandee' | 'en_attente' | 'validee' | 'refusee'
export type OrigineContenu = 'fiche' | 'fichier' | 'manuel' | 'duplication'
export type Piece = 'cv' | 'lm' | 'portfolio' | 'demo'
export type Exigence = 'non' | 'facultatif' | 'obligatoire'

export interface Evenement {
  date: string
  texte: string
}

export interface Fiche {
  id: string
  intitule: string
  service: string
  localisation: string
  categories: string[]
  statuts: string[]
  codePoste: string
  missions: string
  activites: string[]
  competences: string[]
  profil: string
  environnement: string
  teletravail: string
  conditions: string
  origine: OrigineFiche
  /** Fiche récupérée d'un SIRH (simulation) : référence et dernière synchronisation. */
  sirh?: { reference: string, synchroLe: string }
  /** Fiche issue d'un document ajouté (simulation). */
  document?: { nom: string, ajouteLe: string }
  statut: 'active' | 'archivee'
  modifieLe: string
  historique: Evenement[]
}

/** Une validation du circuit : un nom et un ou plusieurs valideurs ; l'accord d'un seul suffit. */
export interface GroupeValidation {
  nom: string
  valideurs: string[]
}

/** Réponse d'une validation sur une offre (circuit figé à la demande). */
export interface ValidationOffre extends GroupeValidation {
  decision: 'attente' | 'accord' | 'refus'
  par?: string
  le?: string
  commentaire?: string
  forcee?: boolean
}

export interface Membre {
  nom: string
  role: 'Responsable' | 'Recruteur' | 'Contributeur'
}

/** Un champ modifié dans une proposition : valeur actuelle, valeur proposée, et la décision du rédacteur. */
export interface ChangementChamp {
  cle: string
  libelle: string
  avant: unknown
  apres: unknown
  statut?: 'acceptee' | 'ignoree'
}

/**
 * Proposition de modification d'un valideur, préparée dans une section et envoyée avec sa décision.
 * Le valideur ne modifie jamais l'offre : la personne qui la rédige accepte ou ignore chaque champ.
 */
export interface Proposition {
  par: string
  le: string
  section: 'annonce' | 'candidature' | 'publication'
  champs: ChangementChamp[]
}

export interface Offre {
  id: string
  /** Fiche de poste rattachée ; vide si l'offre n'en a pas (formulaire vide, offre reprise sans fiche). */
  ficheId: string
  etat: EtatOffre
  origineContenu: OrigineContenu
  sourceOffreId?: string
  /** Personne qui a créé l'offre (par défaut, le compte connecté). */
  creePar?: string

  // Suivi interne — jamais publié, saisi dans l'annonce (encadrés gris). Les données de contexte ne sont jamais recopiées.
  referenceInterne: string
  nbPostes: string
  dateVacance: string
  motifRecrutement: string
  agentRemplace: string
  motifDepart: string
  codePoste: string
  groupeRifseep: string
  cycleTravail: string
  commentaireValideurs: string
  /** Saisi par l'équipe RH (valideurs) pendant la validation. */
  commentaireRH?: string
  referenceFranceTravail?: string
  ficheJointe?: string

  // 2. Annonce — ce que lit le candidat (article D311-8 du CGFP)
  titre: string
  categorie: string
  statutPoste: string
  ouvertA: string[]
  fondementJuridique: string
  metier: string
  competences: string[]
  descriptifEmployeur: string
  presentation: string
  missions: string
  profil: string
  conditions: string
  tempsTravail: string
  /** Rémunération des fonctionnaires. */
  remuneration: string
  remunerationContractuels?: string
  teletravail: string
  lieu: string
  /** Retiré de l'annonce (paramétré dans l'ATS) ; conservé pour les anciennes données. */
  contact: string
  versant?: string
  natureContrat?: string
  niveauExperience?: string
  niveauEtudes?: string
  langues?: string
  management?: string
  corps?: string
  grade?: string
  infosComplementaires?: string

  // 3. Formulaire de candidature
  modeCandidature: 'ats' | 'courriel' | 'externe'
  courrielCandidature: string
  urlCandidature: string
  pieces: Record<Piece, Exigence>
  questions: string[]

  // 4. Processus et 5. Équipe
  processusPersonnalise: boolean
  etapesProcessus: string[]
  equipe: Membre[]

  // 6. Publication : une seule date de fin, qui est aussi la date limite de candidature
  dateDebut: string
  dateFin: string
  urgence: boolean
  diffusion?: 'simple' | 'multi'
  canaux: string[]
  publications: Record<string, { etat: 'publiee' | 'arretee', debut: string, fin: string }>

  // Validation (ancienne DAR)
  validationEtat: EtatValidation
  validations?: ValidationOffre[]
  validationDemandeeLe?: string
  validationObtenueLe?: string
  modifieeDepuisValidation?: boolean
  propositions?: Proposition[]

  notifications: 'chaque' | 'cinq' | 'quotidien' | 'aucune'
  /** Candidatures pas encore ouvertes (fictif, pour la colonne « Action à faire »). */
  nouvellesCandidatures?: number
  creeLe: string
  modifieLe: string
  publieeLe?: string
  retireeLe?: string
  historique: Evenement[]
}

export const LIBELLES_ETAT: Record<EtatOffre, string> = {
  brouillon: 'Brouillon',
  publiee: 'Publiée',
  retiree: 'Retirée',
  archivee: 'Archivée',
}

export const LIBELLES_VALIDATION: Record<EtatValidation, string> = {
  non_demandee: 'Non demandée',
  en_attente: 'En attente',
  validee: 'Validée',
  refusee: 'Refusée',
}

export const LIBELLES_ORIGINE: Record<OrigineFiche, string> = {
  ats: 'Créée dans l\'ATS',
  sirh: 'Récupérée du SIRH',
  document: 'Issue d\'un document',
}

export const LIBELLES_CONTENU: Record<OrigineContenu, string> = {
  fiche: 'Depuis la fiche de poste',
  fichier: 'Depuis un fichier',
  manuel: 'Formulaire vide',
  duplication: 'Duplication d\'une offre',
}

export const PIECES: { id: Piece, label: string }[] = [
  { id: 'cv', label: 'CV' },
  { id: 'lm', label: 'Lettre de motivation' },
  { id: 'portfolio', label: 'Portfolio' },
  { id: 'demo', label: 'Bande démo' },
]

export const CATEGORIES = ['A', 'B', 'C']
export const STATUTS_POSTE = ['Création de poste', 'Poste vacant', 'Poste susceptible d\'être vacant']
export const MOTIFS_RECRUTEMENT = ['Création de poste', 'Remplacement', 'Renouvellement', 'Vacance de poste']
export const MOTIFS_DEPART = ['Mutation', 'Départ à la retraite', 'Fin de contrat', 'Disponibilité', 'Démission']
export const TEMPS_TRAVAIL = [
  { value: 'complet', label: 'Temps complet' },
  { value: 'non_complet', label: 'Temps non complet' },
  { value: 'incomplet', label: 'Temps incomplet' },
]

/** Extrait fictif du référentiel RMFP+ : le métier choisi propose ses compétences, déjà cochées. */
export const METIERS = [
  { id: 'gest-paie', libelle: 'Gestionnaire paie', domaine: 'Ressources humaines', competences: ['Réglementation statutaire et indemnitaire', 'Maîtrise des outils de paie', 'Contrôle des éléments variables', 'Rigueur et confidentialité'] },
  { id: 'charge-recrut', libelle: 'Chargé·e de recrutement', domaine: 'Ressources humaines', competences: ['Techniques de recrutement', 'Statut de la fonction publique', 'Conduite d\'entretien', 'Sens de la relation'] },
  { id: 'cp-si', libelle: 'Chef·fe de projet maîtrise d\'ouvrage SI', domaine: 'Numérique et systèmes d\'information', competences: ['Gestion de projet', 'Expression de besoins', 'Pilotage de prestataires', 'Conduite du changement'] },
  { id: 'assist-admin', libelle: 'Assistant·e administratif·ve', domaine: 'Administration générale', competences: ['Outils bureautiques', 'Organisation', 'Accueil du public', 'Rédaction de courriers'] },
  { id: 'accueil', libelle: 'Chargé·e d\'accueil', domaine: 'Administration générale', competences: ['Accueil physique et téléphonique', 'Orientation du public', 'Gestion des situations difficiles'] },
  { id: 'resp-si', libelle: 'Responsable des systèmes d\'information', domaine: 'Numérique et systèmes d\'information', competences: ['Management d\'équipe', 'Architecture des SI', 'Sécurité des SI', 'Pilotage budgétaire'] },
]
export const metier = (id: string) => METIERS.find(m => m.id === id)
const MOTS_METIER: [string, string][] = [['paie', 'gest-paie'], ['recrutement', 'charge-recrut'], ['projet', 'cp-si'], ['assistant', 'assist-admin'], ['accueil', 'accueil'], ['informatique', 'resp-si']]

/** Support maître : toute publication passe par lui (simple diffusion). */
export const SUPPORT_MAITRE = { id: 'csp', nom: 'Choisir le Service Public', detail: 'Support de publication maître' }
/** Sites partenaires proposés en multi-diffusion (liste indicative, simulée). */
export const SITES_PARTENAIRES = [
  { id: 'intranet', nom: 'Intranet ministériel', detail: 'Visible des agents du ministère' },
  { id: 'pep', nom: 'Place de l\'emploi public', detail: 'Emploi public, tous versants' },
  { id: 'francetravail', nom: 'France Travail', detail: 'Site d\'emploi généraliste' },
  { id: 'apec', nom: 'Apec', detail: 'Postes de cadres' },
  { id: 'linkedin', nom: 'LinkedIn', detail: 'Réseau professionnel' },
]
export const CANAUX_DIFFUSION = [SUPPORT_MAITRE, ...SITES_PARTENAIRES]

/** Paramètres de l'organisme, administrés par le superviseur. */
export interface Organisme {
  nom: string
  superviseur: string
  /** « Faire valider les offres avant publication » : désactivé par défaut. */
  validationActive: boolean
  groupes: GroupeValidation[]
  etapesRecrutement: string[]
  /** Droits des agents : créer des offres, publier, autoriser (peut être désigné valideur). */
  agents: { nom: string, creer: boolean, publier: boolean, autoriser?: boolean }[]
  versant?: string
  journal: Evenement[]
}

export const VERSANTS = ['Fonction publique de l\'État', 'Fonction publique territoriale', 'Fonction publique hospitalière']

export const UTILISATEUR = 'Camille Moreau'

// --- Dates (ISO, relatives à aujourd'hui pour que la démonstration reste juste) ---

export function aujourdhui(): string {
  return iso(new Date())
}
function iso(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
export function plusJours(date: string, n: number): string {
  const d = new Date(`${date}T12:00:00`)
  d.setDate(d.getDate() + n)
  return iso(d)
}
export function plusUnMois(date: string): string {
  const d = new Date(`${date}T12:00:00`)
  d.setMonth(d.getMonth() + 1)
  return iso(d)
}
const J = (n: number) => plusJours(aujourdhui(), n)
/** « 12 novembre 2026 » */
export function dateLongue(date: string): string {
  return date ? new Date(`${date}T12:00:00`).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}
export function joursRestants(date: string): number {
  return Math.round((new Date(`${date}T12:00:00`).getTime() - new Date(`${aujourdhui()}T12:00:00`).getTime()) / 86400000)
}
/** Publiée et se termine sous 7 jours. */
export function termineBientot(o: Offre): boolean {
  return o.etat === 'publiee' && Boolean(o.dateFin) && joursRestants(o.dateFin) <= 7
}

// --- Données fictives ---

function fichesInitiales(): Fiche[] {
  const base = { statut: 'active' as const, teletravail: '', conditions: '', environnement: '', codePoste: '' }
  return [
    {
      ...base,
      id: 'FP-SG-2026-007',
      intitule: 'Gestionnaire de paie',
      service: 'Secrétariat général — Bureau des ressources humaines',
      localisation: 'Toulouse (31)',
      categories: ['B'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'SG-PAIE',
      missions: 'Au sein du BRH, le titulaire assure la pré-liquidation de la paie des agents (tit. et contr.) relevant du périmètre de gestion (env. 900 ag.) en lien avec le CSRH et la DRFiP.',
      activites: ['Saisie et contrôle des EVS dans le SIRH', 'Calcul des IJ, rappels et précomptes', 'Réponse aux sollicitations des agents', 'Participation à la fiabilisation des données de paie'],
      competences: ['Réglementation statutaire et indemnitaire (RIFSEEP)', 'Maîtrise d\'un logiciel de paie', 'Rigueur', 'Discrétion'],
      profil: 'Agent de cat. B ou contractuel ; expérience paie souhaitée.',
      environnement: 'BRH : 12 ETP dont cellule paie 5 ETP. Pics d\'activité liés au calendrier de paie.',
      teletravail: '1 jour par semaine',
      origine: 'ats',
      modifieLe: '2 septembre 2026',
      historique: [{ date: '12 mars 2026', texte: 'Fiche créée dans l\'ATS par Camille Moreau' }, { date: '2 septembre 2026', texte: 'Fiche modifiée — compétences' }],
    },
    {
      ...base,
      id: 'FP-SIRH-48213',
      intitule: 'Chargé·e de recrutement',
      service: 'Secrétariat général — Bureau des ressources humaines',
      localisation: 'Toulouse (31)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'RH-RECR-02',
      missions: 'Piloter les recrutements de la direction : définition des besoins avec les managers, rédaction et diffusion des offres, présélection, organisation des jurys.',
      activites: ['Accompagner les managers dans la définition du besoin', 'Diffuser les offres', 'Présélectionner les candidatures', 'Organiser les entretiens et jurys'],
      competences: ['Techniques de recrutement', 'Statut de la fonction publique', 'Conduite d\'entretien'],
      profil: 'Expérience en recrutement public ou privé.',
      environnement: 'Cellule recrutement de 3 personnes.',
      origine: 'sirh',
      sirh: { reference: 'SIRH-RH-48213', synchroLe: '20 octobre 2026' },
      modifieLe: '20 octobre 2026',
      historique: [{ date: '4 février 2025', texte: 'Fiche récupérée du SIRH ministériel (simulation)' }, { date: '20 octobre 2026', texte: 'Synchronisation SIRH — aucun changement' }],
    },
    {
      ...base,
      id: 'FP-SG-2026-011',
      intitule: 'Juriste marchés publics',
      service: 'Secrétariat général — Pôle juridique',
      localisation: 'Toulouse (31)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'SG-JUR-03',
      missions: 'Sécuriser la commande publique de la direction : conseil aux services, rédaction des pièces de marché, suivi des procédures et des précontentieux.',
      activites: ['Conseiller les services acheteurs', 'Rédiger les pièces administratives des marchés', 'Analyser les offres avec les services', 'Suivre les précontentieux'],
      competences: ['Droit de la commande publique', 'Rédaction juridique', 'Analyse des offres'],
      profil: 'Juriste de formation, expérience en commande publique appréciée.',
      environnement: 'Pôle juridique de 4 personnes.',
      origine: 'ats',
      modifieLe: '5 novembre 2026',
      historique: [{ date: '5 novembre 2026', texte: 'Fiche créée dans l\'ATS par Julien Lefèvre' }],
    },
    {
      ...base,
      id: 'FP-DOC-2026-002',
      intitule: 'Chef·fe de projet numérique',
      service: 'Secrétariat général — Pôle numérique',
      localisation: 'Montpellier (34)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'NUM-CPN',
      missions: 'Conduire les projets de dématérialisation des démarches de la direction, de l\'expression du besoin à la mise en service, en lien avec les métiers et les prestataires.',
      activites: ['Recueillir les besoins des services', 'Piloter les prestataires', 'Accompagner les utilisateurs'],
      competences: ['Gestion de projet agile', 'Connaissance des démarches en ligne', 'Animation de réunions'],
      profil: '',
      teletravail: '2 jours par semaine',
      origine: 'document',
      document: { nom: 'fiche_poste_CPN_v3.docx', ajouteLe: '14 octobre 2026' },
      modifieLe: '14 octobre 2026',
      historique: [{ date: '14 octobre 2026', texte: 'Fiche constituée à partir du document fiche_poste_CPN_v3.docx (extraction simulée)' }],
    },
    {
      ...base,
      id: 'FP-SG-2025-031',
      intitule: 'Assistant·e administratif·ve',
      service: 'Service Aménagement',
      localisation: 'Toulouse (31)',
      categories: ['C'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'SA-ASSIST',
      missions: 'Assurer l\'accueil et le secrétariat du service : courrier, agendas, préparation des dossiers et des réunions.',
      activites: ['Gérer le courrier et les agendas', 'Préparer les réunions', 'Accueillir le public'],
      competences: ['Outils bureautiques', 'Organisation', 'Sens de l\'accueil'],
      profil: 'Expérience en secrétariat appréciée.',
      origine: 'ats',
      modifieLe: '3 juin 2025',
      historique: [{ date: '3 juin 2025', texte: 'Fiche créée dans l\'ATS par Nadia Benali' }],
    },
    {
      ...base,
      id: 'FP-SG-2024-031',
      intitule: 'Responsable informatique',
      service: 'Secrétariat général — Pôle numérique',
      localisation: 'Toulouse (31)',
      categories: ['A'],
      statuts: ['titulaire', 'contractuel'],
      codePoste: 'NUM-RESP',
      missions: 'Encadrer le pôle numérique (6 agents) et garantir le bon fonctionnement du système d\'information de la direction.',
      activites: ['Encadrer le pôle', 'Piloter le budget informatique', 'Assurer la sécurité du système d\'information'],
      competences: ['Management', 'Architecture des systèmes d\'information', 'Sécurité informatique'],
      profil: '',
      origine: 'sirh',
      sirh: { reference: 'SIRH-NUM-30117', synchroLe: '20 octobre 2026' },
      modifieLe: '3 avril 2026',
      historique: [{ date: '3 avril 2026', texte: 'Fiche récupérée du SIRH ministériel (simulation)' }],
    },
    {
      ...base,
      id: 'FP-SG-2023-010',
      intitule: 'Chargé·e d\'accueil',
      service: 'Secrétariat général',
      localisation: 'Toulouse (31)',
      categories: ['C'],
      statuts: ['titulaire'],
      codePoste: 'SG-ACC',
      missions: 'Accueillir et orienter les visiteurs et les appels.',
      activites: [],
      competences: ['Sens de l\'accueil'],
      profil: '',
      origine: 'ats',
      statut: 'archivee',
      modifieLe: '10 janvier 2026',
      historique: [{ date: '2 mai 2023', texte: 'Fiche créée dans l\'ATS' }, { date: '10 janvier 2026', texte: 'Fiche archivée (accueil mutualisé)' }],
    },
  ]
}

const ETAPES_RECRUTEMENT = ['Candidature reçue', 'Présélection', 'Entretien', 'Proposition', 'Recrutement']

/** Champs de contexte : propres à un recrutement, jamais recopiés (ni depuis une fiche, ni en dupliquant). */
function contexteVide() {
  return {
    referenceInterne: '',
    nbPostes: '1',
    dateVacance: '',
    motifRecrutement: '',
    agentRemplace: '',
    motifDepart: '',
    codePoste: '',
    groupeRifseep: '',
    cycleTravail: '',
    commentaireValideurs: '',
    ficheJointe: undefined as string | undefined,
    dateDebut: '',
    dateFin: '',
    urgence: false,
  }
}

function socle() {
  return {
    ...contexteVide(),
    ouvertA: ['titulaire', 'contractuel'],
    fondementJuridique: '',
    descriptifEmployeur: 'La DREAL Occitanie met en œuvre les politiques de l\'État en matière de transition écologique, d\'énergie et de logement.',
    conditions: '',
    tempsTravail: 'complet',
    versant: 'Fonction publique de l\'État',
    remuneration: '',
    remunerationContractuels: '',
    teletravail: '',
    contact: '',
    modeCandidature: 'ats' as const,
    courrielCandidature: '',
    urlCandidature: '',
    pieces: { cv: 'obligatoire', lm: 'facultatif', portfolio: 'non', demo: 'non' } as Record<Piece, Exigence>,
    questions: [] as string[],
    processusPersonnalise: false,
    etapesProcessus: [...ETAPES_RECRUTEMENT],
    equipe: [{ nom: UTILISATEUR, role: 'Responsable' as const }],
    canaux: ['csp'],
    publications: {} as Offre['publications'],
    validationEtat: 'non_demandee' as EtatValidation,
    notifications: 'chaque' as const,
  }
}

const BUDGET: GroupeValidation = { nom: 'Bureau budget', valideurs: ['Anne Dubois', 'Paul Martin'] }
const RECRUTEMENT: GroupeValidation = { nom: 'Bureau recrutement', valideurs: ['Claire Morel'] }

/**
 * Offre « Juriste marchés publics » créée par un collègue, que Camille Moreau (le compte connecté) doit valider.
 * Remise à cet état à chaque chargement du prototype, pour pouvoir rejouer la validation.
 */
function offreJuriste(): Offre {
  return {
    ...socle(),
    id: 'OFF-2026-0153',
    ficheId: 'FP-SG-2026-011',
    etat: 'brouillon',
    origineContenu: 'fiche',
    creePar: 'Julien Lefèvre',
    equipe: [{ nom: 'Julien Lefèvre', role: 'Responsable' }],
    titre: 'Juriste marchés publics',
    categorie: 'A',
    statutPoste: 'Poste vacant',
    metier: '',
    presentation: 'Au sein du pôle juridique, vous sécurisez les achats de la DREAL Occitanie et accompagnez les services dans leurs projets.',
    missions: '- Conseiller les services acheteurs\n- Rédiger les pièces administratives des marchés\n- Analyser les offres avec les services\n- Suivre les précontentieux',
    profil: 'Juriste de formation, vous avez une première expérience en commande publique.',
    competences: ['Droit de la commande publique', 'Rédaction juridique', 'Analyse des offres'],
    lieu: 'Toulouse (31)',
    remuneration: 'Selon expérience, grille indiciaire de catégorie A',
    teletravail: '2 jours par semaine',
    dateVacance: J(45),
    nbPostes: '1',
    motifRecrutement: 'Création de poste',
    codePoste: 'SG-JUR-03',
    groupeRifseep: 'Groupe 3',
    commentaireValideurs: 'Création validée au dialogue de gestion 2026 ; poste financé sur le BOP 217.',
    validationEtat: 'en_attente',
    validationDemandeeLe: dateLongue(J(-2)),
    validations: [
      { ...BUDGET, decision: 'accord', par: 'Paul Martin', le: dateLongue(J(-1)) },
      { nom: 'Pôle juridique', valideurs: [UTILISATEUR], decision: 'attente' },
    ],
    creeLe: '5 novembre 2026',
    modifieLe: 'Hier, 11:20',
    historique: [
      { date: '5 novembre 2026', texte: 'Offre créée par Julien Lefèvre depuis la fiche FP-SG-2026-011' },
      { date: 'Avant-hier', texte: 'Validation demandée (Bureau budget, Pôle juridique)' },
      { date: 'Hier, 11:20', texte: 'Accord du Bureau budget (Paul Martin)' },
    ],
  } as Offre
}

/** Offre que le compte connecté doit valider : créée par quelqu'un d'autre, validation demandée, il fait partie des valideurs. */
export function aValiderParMoi(o: Offre): boolean {
  return Boolean(o.creePar) && o.creePar !== UTILISATEUR && o.validationEtat === 'en_attente'
    && (o.validations ?? []).some(v => v.decision === 'attente' && v.valideurs.includes(UTILISATEUR))
}

function offresInitiales(f: Fiche[]): Offre[] {
  const fiche = (id: string) => f.find(x => x.id === id)!
  return [
    offreJuriste(),
    {
      ...socle(),
      ...contenuDepuisFiche(fiche('FP-SG-2026-007')),
      id: 'OFF-2026-0151',
      ficheId: 'FP-SG-2026-007',
      etat: 'brouillon',
      origineContenu: 'fiche',
      nbPostes: '3',
      motifRecrutement: 'Remplacement',
      motifDepart: 'Départ à la retraite',
      codePoste: 'SG-PAIE',
      creeLe: 'Hier',
      modifieLe: 'Hier, 16:12',
      historique: [{ date: 'Hier, 15:58', texte: 'Offre créée depuis la fiche FP-SG-2026-007' }, { date: 'Hier, 16:12', texte: 'Brouillon enregistré' }],
    },
    {
      ...socle(),
      ...contenuDepuisFiche(fiche('FP-SIRH-48213')),
      presentation: 'Vous rejoignez la cellule recrutement de la DREAL Occitanie et accompagnez les managers pour attirer les bons profils.',
      id: 'OFF-2026-0148',
      ficheId: 'FP-SIRH-48213',
      etat: 'brouillon',
      origineContenu: 'fiche',
      statutPoste: 'Poste vacant',
      dateVacance: J(30),
      motifRecrutement: 'Remplacement',
      agentRemplace: 'Martine Leroy',
      motifDepart: 'Mutation',
      codePoste: 'RH-RECR-02',
      groupeRifseep: 'Groupe 2',
      commentaireValideurs: 'Remplacement à l\'identique, poste budgété.',
      remuneration: 'Selon expérience et grille indiciaire',
      propositions: [{ par: 'Anne Dubois', le: '20 octobre 2026', section: 'annonce', champs: [
        { cle: 'remunerationContractuels', libelle: 'Rémunération des contractuels', avant: '', apres: 'De 2 600 à 3 200 € brut mensuel selon expérience' },
        { cle: 'teletravail', libelle: 'Télétravail', avant: '', apres: '2 jours par semaine' },
      ] }],
      validationEtat: 'en_attente',
      validationDemandeeLe: '17 octobre 2026',
      validations: [
        { ...BUDGET, decision: 'accord', par: 'Anne Dubois', le: '20 octobre 2026', commentaire: 'D\'accord. Je propose de préciser la rémunération des contractuels et le télétravail.' },
        { ...RECRUTEMENT, decision: 'attente' },
      ],
      creeLe: '15 octobre 2026',
      modifieLe: '20 octobre 2026',
      historique: [
        { date: '15 octobre 2026', texte: 'Offre créée depuis la fiche FP-SIRH-48213' },
        { date: '17 octobre 2026', texte: 'Validation demandée (Bureau budget, Bureau recrutement)' },
        { date: '20 octobre 2026', texte: 'Accord du Bureau budget (Anne Dubois)' },
      ],
    },
    {
      ...socle(),
      ...contenuDepuisFiche(fiche('FP-DOC-2026-002')),
      titre: 'Chef·fe de projet numérique — démarches en ligne',
      presentation: 'Vous faites entrer les démarches de la DREAL dans l\'ère du numérique : vos projets simplifient la vie des usagers et des agents.',
      profil: 'Vous avez conduit des projets numériques et savez faire travailler ensemble métiers et prestataires.',
      id: 'OFF-2026-0145',
      ficheId: 'FP-DOC-2026-002',
      etat: 'brouillon',
      origineContenu: 'fiche',
      statutPoste: 'Création de poste',
      dateVacance: J(45),
      fondementJuridique: 'Article L332-2 (besoins permanents)',
      motifRecrutement: 'Création de poste',
      remuneration: 'Selon expérience, de 2 600 à 3 400 € brut mensuel',
      contact: 'Pôle numérique — recrutement.num@exemple.gouv.fr',
      questions: ['Quel projet numérique vous a le plus appris, et pourquoi ?'],
      equipe: [{ nom: UTILISATEUR, role: 'Responsable' }, { nom: 'Julien Lefèvre', role: 'Recruteur' }],
      dateDebut: J(1),
      dateFin: plusUnMois(J(1)),
      validationEtat: 'validee',
      validationDemandeeLe: '9 octobre 2026',
      validationObtenueLe: '15 octobre 2026',
      validations: [
        { ...BUDGET, decision: 'accord', par: 'Paul Martin', le: '12 octobre 2026' },
        { ...RECRUTEMENT, decision: 'accord', par: 'Claire Morel', le: '15 octobre 2026' },
      ],
      creeLe: '8 octobre 2026',
      modifieLe: '16 octobre 2026',
      historique: [
        { date: '8 octobre 2026', texte: 'Offre créée depuis la fiche FP-DOC-2026-002' },
        { date: '9 octobre 2026', texte: 'Validation demandée (Bureau budget, Bureau recrutement)' },
        { date: '12 octobre 2026', texte: 'Accord du Bureau budget (Paul Martin)' },
        { date: '15 octobre 2026', texte: 'Accord du Bureau recrutement (Claire Morel) — validation obtenue' },
      ],
    },
    {
      ...socle(),
      ...contenuDepuisFiche(fiche('FP-SG-2025-031')),
      titre: 'Assistant·e administratif·ve au service Aménagement',
      presentation: 'Au cœur d\'un service de 25 personnes, vous êtes le premier contact des usagers et le point d\'appui de l\'équipe.',
      id: 'OFF-2026-0118',
      nouvellesCandidatures: 5,
      ficheId: 'FP-SG-2025-031',
      etat: 'publiee',
      origineContenu: 'fiche',
      statutPoste: 'Poste vacant',
      dateVacance: J(-10),
      fondementJuridique: 'Article L332-2 (besoins permanents)',
      motifRecrutement: 'Vacance de poste',
      remuneration: 'Grille indiciaire de catégorie C',
      contact: 'Nadia Benali, responsable recrutement',
      dateDebut: J(-26),
      dateFin: J(4),
      diffusion: 'multi',
      canaux: ['csp', 'intranet'],
      publications: {
        csp: { etat: 'publiee', debut: dateLongue(J(-26)), fin: J(4) },
        intranet: { etat: 'publiee', debut: dateLongue(J(-26)), fin: J(4) },
      },
      validationEtat: 'validee',
      validationObtenueLe: '29 septembre 2026',
      validations: [
        { ...BUDGET, decision: 'accord', par: 'Anne Dubois', le: '25 septembre 2026' },
        { ...RECRUTEMENT, decision: 'accord', par: 'Claire Morel', le: '29 septembre 2026' },
      ],
      creeLe: '18 septembre 2026',
      modifieLe: dateLongue(J(-26)),
      publieeLe: dateLongue(J(-26)),
      historique: [
        { date: '18 septembre 2026', texte: 'Offre créée depuis la fiche FP-SG-2025-031' },
        { date: '22 septembre 2026', texte: 'Validation demandée (Bureau budget, Bureau recrutement)' },
        { date: '29 septembre 2026', texte: 'Validation obtenue' },
        { date: dateLongue(J(-26)), texte: 'Offre publiée sur Choisir le Service Public et l\'intranet' },
      ],
    },
    {
      ...socle(),
      ...contenuDepuisFiche(fiche('FP-SG-2023-010')),
      id: 'OFF-2025-0087',
      ficheId: 'FP-SG-2023-010',
      etat: 'archivee',
      origineContenu: 'manuel',
      nbPostes: '2',
      dateDebut: '2025-05-20',
      dateFin: '2025-06-30',
      publications: { csp: { etat: 'arretee', debut: '20 mai 2025', fin: '2025-06-30' } },
      validationEtat: 'validee',
      creeLe: '2 mai 2025',
      modifieLe: '15 juillet 2025',
      publieeLe: '20 mai 2025',
      retireeLe: '30 juin 2025',
      historique: [
        { date: '2 mai 2025', texte: 'Offre créée (formulaire vide)' },
        { date: '20 mai 2025', texte: 'Offre publiée' },
        { date: '30 juin 2025', texte: 'Retrait automatique à la date limite' },
        { date: '15 juillet 2025', texte: 'Offre archivée (2 postes pourvus)' },
      ],
    },
  ]
}

/** Contenu de l'annonce proposé à partir d'une fiche : repris tel quel, à adapter pour les candidats. */
export function contenuDepuisFiche(f: Fiche): Pick<Offre, 'titre' | 'categorie' | 'statutPoste' | 'metier' | 'competences' | 'presentation' | 'missions' | 'profil' | 'lieu' | 'teletravail' | 'conditions'> {
  const cle = MOTS_METIER.find(([mot]) => f.intitule.toLowerCase().includes(mot))?.[1]
  const m = METIERS.find(x => x.id === cle)
  return {
    titre: f.intitule,
    categorie: f.categories[0] ?? '',
    statutPoste: '',
    metier: m?.id ?? '',
    competences: [...(m?.competences ?? []), ...f.competences.filter(c => !m?.competences.includes(c))],
    presentation: f.environnement,
    missions: [f.missions, ...f.activites.map(a => `- ${a}`)].filter(Boolean).join('\n'),
    profil: f.profil,
    lieu: f.localisation,
    teletravail: f.teletravail,
    conditions: f.conditions,
  }
}

// --- Stockage de session ---

const CLE = 'csplab-proto-ats-v15'

interface Base { fiches: Fiche[], offres: Offre[], organisme: Organisme, role: 'recruteur' | 'superviseur' }

function lire(): Base | null {
  try {
    const brut = sessionStorage.getItem(CLE)
    return brut ? JSON.parse(brut) : null
  }
  catch {
    return null
  }
}

function organismeInitial(): Organisme {
  return {
    nom: 'DREAL Occitanie',
    versant: 'Fonction publique de l\'État',
    superviseur: 'Isabelle Fournier',
    validationActive: true,
    groupes: [{ ...BUDGET, valideurs: [...BUDGET.valideurs] }, { ...RECRUTEMENT, valideurs: [...RECRUTEMENT.valideurs] }],
    etapesRecrutement: [...ETAPES_RECRUTEMENT],
    agents: [
      { nom: 'Camille Moreau', creer: true, publier: true, autoriser: true },
      { nom: 'Nadia Benali', creer: true, publier: true, autoriser: false },
      { nom: 'Julien Lefèvre', creer: true, publier: false, autoriser: false },
      { nom: 'Anne Dubois', creer: false, publier: false, autoriser: true },
      { nom: 'Paul Martin', creer: false, publier: false, autoriser: true },
      { nom: 'Claire Morel', creer: true, publier: true, autoriser: true },
      { nom: 'Hélène Robert', creer: false, publier: false, autoriser: false },
    ],
    journal: [
      { date: '3 septembre 2026', texte: 'Circuit de validation activé par Isabelle Fournier' },
      { date: '3 septembre 2026', texte: 'Validations « Bureau budget » et « Bureau recrutement » ajoutées' },
    ],
  }
}

function initial(): Base {
  const fiches = fichesInitiales()
  return { fiches, offres: offresInitiales(fiches), organisme: organismeInitial(), role: 'recruteur' }
}

export const db = reactive(lire() ?? initial())

// À chaque chargement, l'offre « Juriste marchés publics » redevient « à valider par Camille ».
{
  const i = db.offres.findIndex(o => o.id === 'OFF-2026-0153')
  if (i >= 0) {
    db.offres.splice(i, 1, offreJuriste())
  }
  else {
    db.offres.unshift(offreJuriste())
  }
}

export function sauvegarder() {
  try {
    sessionStorage.setItem(CLE, JSON.stringify(db))
  }
  catch {
    // Stockage indisponible : le prototype reste utilisable, sans persistance.
  }
}

export function reinitialiser() {
  const neuf = initial()
  db.fiches.splice(0, db.fiches.length, ...neuf.fiches)
  db.offres.splice(0, db.offres.length, ...neuf.offres)
  Object.assign(db.organisme, neuf.organisme)
  db.role = 'recruteur'
  sauvegarder()
}

export function heure(): string {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

/** « le 12 octobre 2026 » ou « aujourd'hui, 14:25 ». */
export function le(date: string | undefined): string {
  if (!date) {
    return ''
  }
  return /^(?:Aujourd'hui|Hier)/.test(date) ? date.charAt(0).toLowerCase() + date.slice(1) : `le ${date}`
}

const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

/** Clé de tri d'une date affichée (« 12 octobre 2026 », « Hier, 16:12 », « Aujourd'hui, 14:25 »). */
export function dateTri(date: string): string {
  if (date.startsWith('Aujourd')) {
    return `9-${date.slice(-5)}`
  }
  if (date.startsWith('Hier')) {
    return `8-${date.slice(-5)}`
  }
  const [j, m, a] = date.split(' ')
  return `${a}-${String(MOIS.indexOf(m ?? '') + 1).padStart(2, '0')}-${(j ?? '').padStart(2, '0')}`
}

export function maintenant(): string {
  return `Aujourd'hui, ${heure()}`
}

export const fiche = (id: string) => db.fiches.find(f => f.id === id)
export const offre = (id: string) => db.offres.find(o => o.id === id)
export const offresDe = (ficheId: string) => db.offres.filter(o => o.ficheId === ficheId)

function journal(o: Offre, texte: string) {
  o.modifieLe = maintenant()
  o.historique.push({ date: maintenant(), texte })
  sauvegarder()
}

function prochainNumero(prefixe: string, liste: { id: string }[], min = 150) {
  const max = Math.max(min, ...liste.map(x => Number(x.id.slice(-3)) || 0))
  return `${prefixe}${String(max + 1).padStart(3, '0')}`
}

export function nouvelleFiche(partiel: Partial<Fiche>, origine: OrigineFiche, evenement: string): Fiche {
  const f: Fiche = {
    id: prochainNumero('FP-SG-2026-', db.fiches.filter(x => x.id.startsWith('FP-SG-2026-')), 0),
    intitule: '',
    service: '',
    localisation: '',
    categories: [],
    statuts: [],
    codePoste: '',
    missions: '',
    activites: [],
    competences: [],
    profil: '',
    environnement: '',
    teletravail: '',
    conditions: '',
    origine,
    statut: 'active',
    modifieLe: maintenant(),
    historique: [{ date: maintenant(), texte: evenement }],
    ...partiel,
  }
  if (origine === 'document') {
    f.id = prochainNumero('FP-DOC-2026-', db.fiches.filter(x => x.id.startsWith('FP-DOC-2026-')), 0)
  }
  db.fiches.unshift(f)
  sauvegarder()
  return f
}

/** Les données de contexte (informations internes, dates de publication) ne sont jamais reprises. */
/**
 * Nouvelle offre : depuis une fiche (contenu proposé), un formulaire vide (saisie de départ) ou une offre reprise.
 * La fiche est facultative. Les données de contexte (date de vacance, motif, agent remplacé, code poste,
 * nombre de postes, dates, commentaires de validation) ne sont jamais reprises.
 */
export function nouvelleOffre(f: Fiche | undefined, origineContenu: OrigineContenu, depuis?: Offre, saisie?: Partial<Offre>): Offre {
  const annonce = depuis
    ? {
        titre: depuis.titre,
        categorie: depuis.categorie,
        statutPoste: depuis.statutPoste,
        ouvertA: [...depuis.ouvertA],
        fondementJuridique: depuis.fondementJuridique,
        metier: depuis.metier,
        competences: [...depuis.competences],
        descriptifEmployeur: depuis.descriptifEmployeur,
        presentation: depuis.presentation,
        missions: depuis.missions,
        profil: depuis.profil,
        conditions: depuis.conditions,
        tempsTravail: depuis.tempsTravail,
        remuneration: depuis.remuneration,
        remunerationContractuels: depuis.remunerationContractuels,
        teletravail: depuis.teletravail,
        lieu: depuis.lieu,
        versant: depuis.versant,
        natureContrat: depuis.natureContrat,
        niveauExperience: depuis.niveauExperience,
        niveauEtudes: depuis.niveauEtudes,
        langues: depuis.langues,
        management: depuis.management,
        corps: depuis.corps,
        grade: depuis.grade,
        infosComplementaires: depuis.infosComplementaires,
        modeCandidature: depuis.modeCandidature,
        courrielCandidature: depuis.courrielCandidature,
        urlCandidature: depuis.urlCandidature,
        pieces: { ...depuis.pieces },
        questions: [...depuis.questions],
      }
    : f ? contenuDepuisFiche(f) : ({ titre: '', categorie: '', statutPoste: '', metier: '', competences: [], presentation: '', missions: '', profil: '', lieu: '', ...saisie } as Partial<Offre>)
  const texte = {
    fiche: `Offre créée depuis la fiche ${f?.id}`,
    fichier: `Offre créée depuis un fichier (fiche ${f?.id})`,
    manuel: 'Offre créée depuis un formulaire vide, sans fiche de poste',
    duplication: `Offre créée par duplication de ${depuis?.id} — données de contexte non reprises`,
  }[origineContenu]
  const o = {
    ...socle(),
    ...annonce,
    id: `OFF-2026-0${prochainNumero('', db.offres.filter(x => x.id.startsWith('OFF-2026-')))}`,
    ficheId: f?.id ?? '',
    etat: 'brouillon',
    origineContenu,
    sourceOffreId: depuis?.id,
    creeLe: maintenant(),
    modifieLe: maintenant(),
    historique: [{ date: maintenant(), texte }],
  } as Offre
  db.offres.unshift(o)
  f?.historique.push({ date: maintenant(), texte: `Offre ${o.id} rattachée` })
  sauvegarder()
  return o
}

// --- Propositions de modification des valideurs ---

/** Champs suivis par section, avec leur libellé, pour calculer les différences d'une proposition. */
export const CHAMPS_SECTION: Record<Proposition['section'], Record<string, string>> = {
  annonce: {
    titre: 'Titre de l\'offre',
    versant: 'Versant',
    nbPostes: 'Nombre de postes',
    lieu: 'Lieu',
    ouvertA: 'Nature de l\'emploi',
    categorie: 'Catégorie',
    fondementJuridique: 'Fondement juridique',
    natureContrat: 'Nature du contrat',
    statutPoste: 'Statut du poste',
    dateVacance: 'Date de vacance',
    corps: 'Corps',
    grade: 'Grade',
    tempsTravail: 'Temps de travail',
    teletravail: 'Télétravail',
    management: 'Management',
    remuneration: 'Rémunération des fonctionnaires',
    remunerationContractuels: 'Rémunération des contractuels',
    conditions: 'Conditions particulières',
    referenceInterne: 'Référence interne',
    referenceFranceTravail: 'Référence France Travail',
    codePoste: 'Code poste',
    motifRecrutement: 'Motif de recrutement',
    motifDepart: 'Motif de départ',
    agentRemplace: 'Agent remplacé',
    groupeRifseep: 'Groupe RIFSEEP',
    cycleTravail: 'Cycle de travail',
    descriptifEmployeur: 'Description de l\'employeur',
    presentation: 'Descriptif du service',
    missions: 'Missions',
    metier: 'Métier',
    competences: 'Compétences',
    profil: 'Expérience et diplômes attendus',
    niveauExperience: 'Niveau d\'expérience',
    niveauEtudes: 'Niveau d\'études',
    langues: 'Langues',
    infosComplementaires: 'Informations complémentaires',
  },
  candidature: { modeCandidature: 'Mode de candidature', courrielCandidature: 'Adresse de réception', urlCandidature: 'Lien de candidature', pieces: 'Pièces demandées', questions: 'Questions aux candidats' },
  publication: { dateDebut: 'Début de publication', dateFin: 'Fin de publication', urgence: 'Recrutement urgent', diffusion: 'Type de diffusion', canaux: 'Sites de diffusion' },
}

/** Différences entre l'offre et la copie modifiée par le valideur, pour une section. */
export function differences(o: Offre, copie: Offre, section: Proposition['section']): ChangementChamp[] {
  const champs = CHAMPS_SECTION[section]
  const rec = (x: Offre) => x as unknown as Record<string, unknown>
  return Object.entries(champs)
    .filter(([cle]) => JSON.stringify(rec(o)[cle] ?? '') !== JSON.stringify(rec(copie)[cle] ?? ''))
    .map(([cle, libelle]) => ({ cle, libelle, avant: rec(o)[cle] ?? '', apres: JSON.parse(JSON.stringify(rec(copie)[cle] ?? '')) }))
}

/** Valeur lisible d'un champ (listes, pièces, booléens). */
export function valeurLisible(v: unknown): string {
  if (Array.isArray(v)) {
    return v.length ? v.join(', ') : '(vide)'
  }
  if (v && typeof v === 'object') {
    return Object.entries(v as Record<string, string>).map(([k, x]) => `${k} : ${x}`).join(', ')
  }
  if (typeof v === 'boolean') {
    return v ? 'Oui' : 'Non'
  }
  return v === '' || v === undefined || v === null ? '(vide)' : String(v)
}

export function decider(o: Offre, ip: number, ic: number, statut: 'acceptee' | 'ignoree') {
  const c = o.propositions?.[ip]?.champs[ic]
  if (!c) {
    return
  }
  c.statut = statut
  if (statut === 'acceptee') {
    (o as unknown as Record<string, unknown>)[c.cle] = JSON.parse(JSON.stringify(c.apres))
  }
  journal(o, `${statut === 'acceptee' ? 'Proposition acceptée' : 'Proposition ignorée'} (${o.propositions![ip]!.par}) : ${c.libelle}`)
}

// --- Circuit de validation (ancienne DAR) ---

/** Disponible à tout moment, dès le brouillon, sans champ minimum. Les accords déjà donnés restent acquis. */
export function demanderValidation(o: Offre) {
  const avant = o.validations ?? []
  o.validations = db.organisme.groupes.map((g) => {
    const acquis = avant.find(v => v.nom === g.nom && v.decision === 'accord')
    return acquis ?? { nom: g.nom, valideurs: [...g.valideurs], decision: 'attente' }
  })
  o.validationEtat = o.validations.every(v => v.decision === 'accord') ? 'validee' : 'en_attente'
  o.validationDemandeeLe = maintenant()
  o.modifieeDepuisValidation = false
  journal(o, `Validation demandée (${o.validations.map(v => v.nom).join(', ')})`)
}

/** Un refus demande un commentaire. Toutes les validations sont requises ; elles se font en parallèle. */
export function repondre(o: Offre, i: number, decision: 'accord' | 'refus', par: string, commentaire?: string, propositions: Proposition[] = []) {
  const v = o.validations![i]!
  if (propositions.length) {
    o.propositions = [...(o.propositions ?? []), ...propositions]
    journal(o, `${propositions.reduce((n, p) => n + p.champs.length, 0)} modification(s) proposée(s) par ${par}`)
  }
  v.decision = decision
  v.par = par
  v.le = maintenant()
  v.commentaire = commentaire
  if (decision === 'refus') {
    o.validationEtat = 'refusee'
    journal(o, `Refus du ${v.nom} (${par}) : « ${commentaire} »`)
  }
  else if (o.validations!.every(x => x.decision === 'accord')) {
    o.validationEtat = 'validee'
    o.validationObtenueLe = maintenant()
    journal(o, `Accord du ${v.nom} (${par})${commentaire ? ` : « ${commentaire} »` : ''} — validation obtenue`)
  }
  else {
    journal(o, `Accord du ${v.nom} (${par})${commentaire ? ` : « ${commentaire} »` : ''}`)
  }
}

/** Le superviseur peut valider à la place des valideurs : « validation forcée ». */
export function forcerValidation(o: Offre) {
  for (const v of o.validations ?? []) {
    if (v.decision !== 'accord') {
      Object.assign(v, { decision: 'accord', par: db.organisme.superviseur, le: maintenant(), forcee: true })
    }
  }
  o.validationEtat = 'validee'
  o.validationObtenueLe = maintenant()
  journal(o, `Validation forcée par ${db.organisme.superviseur} (superviseur)`)
}

/** Une modification après validation ne relance pas le circuit : elle est signalée et journalisée. */
export function signalerModification(o: Offre) {
  if (o.validationEtat === 'validee' && o.etat === 'brouillon' && !o.modifieeDepuisValidation) {
    o.modifieeDepuisValidation = true
    o.historique.push({ date: maintenant(), texte: 'Offre modifiée depuis la validation' })
  }
}

/** Validation requise par l'organisme et pas encore obtenue. */
export function validationManquante(o: Offre): boolean {
  return db.organisme.validationActive && o.validationEtat !== 'validee'
}

// --- Publication (toujours décidée par une personne qui a le droit « Publier ») ---

export function publier(o: Offre, diffusion: 'simple' | 'multi', partenaires: string[]) {
  o.diffusion = diffusion
  o.canaux = [SUPPORT_MAITRE.id, ...(diffusion === 'multi' ? partenaires : [])]
  for (const id of o.canaux) {
    o.publications[id] = { etat: 'publiee', debut: dateLongue(o.dateDebut), fin: o.dateFin }
  }
  o.etat = 'publiee'
  o.publieeLe = maintenant()
  const noms = CANAUX_DIFFUSION.filter(c => o.canaux.includes(c.id)).map(c => c.nom).join(', ')
  journal(o, `Offre publiée du ${dateLongue(o.dateDebut)} au ${dateLongue(o.dateFin)} sur ${noms}`)
}

/** Prolonger : nouvelle date limite, sans nouvelle validation. */
export function prolonger(o: Offre, nouvelleFin: string) {
  o.dateFin = nouvelleFin
  for (const p of Object.values(o.publications)) {
    if (p.etat === 'publiee') {
      p.fin = nouvelleFin
    }
  }
  journal(o, `Publication prolongée jusqu'au ${dateLongue(nouvelleFin)}`)
}

/** Retirer ne clôt pas le recrutement : les candidatures restent à traiter. */
export function retirer(o: Offre, mode: 'automatique' | 'manuel' | 'urgence') {
  for (const p of Object.values(o.publications)) {
    p.etat = 'arretee'
  }
  o.etat = 'retiree'
  o.retireeLe = maintenant()
  journal(o, { automatique: 'Retrait automatique à la date limite', manuel: 'Offre retirée', urgence: 'Offre retirée en urgence (avant un mois)' }[mode])
}

export function arreterSupport(o: Offre, id: string) {
  const p = o.publications[id]
  if (p) {
    p.etat = 'arretee'
    journal(o, `Publication arrêtée : ${CANAUX_DIFFUSION.find(c => c.id === id)?.nom}`)
  }
}

export function archiverOffre(o: Offre) {
  for (const p of Object.values(o.publications)) {
    p.etat = 'arretee'
  }
  o.etat = 'archivee'
  journal(o, 'Offre archivée')
}

/** Simule le retrait automatique des offres dont la date limite est passée. */
export function retraitsAutomatiques() {
  for (const o of db.offres) {
    if (o.etat === 'publiee' && o.dateFin && joursRestants(o.dateFin) < 0) {
      retirer(o, 'automatique')
    }
  }
}
