// Domaine autonome du prototype : ne dépend pas des types API générés (@/types/api),
// qui modélisent le côté recruteur. Le candidat a son propre vocabulaire.

export type TypeContrat = 'Titulaire (mutation, détachement)' | 'Contractuel CDD' | 'Contractuel CDI'

export type StatutOffre = 'ouverte' | 'pourvue' | 'cloturee'

export interface InformationPratique {
  label: string
  valeur: string
}

export interface Offre {
  id: string
  intitule: string
  organisme: string
  service?: string
  localisation: string
  typeContrat: TypeContrat
  remunerationMin: number
  remunerationMax: number
  remunerationDetail: string
  statut: StatutOffre
  dateLimiteCandidature: string
  reference: string
  description: string
  missions: string[]
  profilRecherche: string[]
  informationsPratiques: InformationPratique[]
  etapesProcessus: string[]
}

export const offrePrincipale: Offre = {
  id: 'offre-innovation-numerique',
  intitule: 'Chargé·e de mission innovation numérique',
  organisme: 'Ministère de la Transformation et de la Fonction Publiques',
  service: 'Direction interministérielle du numérique',
  localisation: 'Paris 7ᵉ (télétravail partiel possible)',
  typeContrat: 'Contractuel CDD',
  remunerationMin: 38000,
  remunerationMax: 45000,
  remunerationDetail: '38 000 € à 45 000 € brut annuel, selon expérience',
  statut: 'ouverte',
  dateLimiteCandidature: '6 octobre 2026',
  reference: 'DINUM-2026-0142',
  description: 'Au sein de la direction interministérielle du numérique, vous rejoignez une équipe '
    + 'chargée d\'accompagner les administrations dans la conception de services publics numériques '
    + 'plus simples et plus rapides à utiliser. Vous travaillerez en lien direct avec les équipes produit '
    + 'des ministères partenaires.',
  missions: [
    'Accompagner 3 à 5 administrations dans l\'amélioration de leurs démarches en ligne',
    'Animer des ateliers de recherche utilisateur et restituer les enseignements',
    'Rédiger des recommandations d\'usage et de design de service',
    'Contribuer à la doctrine interministérielle sur l\'accessibilité numérique',
  ],
  profilRecherche: [
    'Expérience en conduite de projet ou en accompagnement au changement',
    'Sensibilité aux enjeux de service public et d\'accessibilité',
    'À l\'aise pour animer des ateliers avec des interlocuteurs variés',
    'Une première expérience en UX ou en produit numérique est un plus',
  ],
  informationsPratiques: [
    { label: 'Prise de poste', valeur: 'Dès que possible' },
    { label: 'Durée du contrat', valeur: '3 ans, renouvelable' },
    { label: 'Temps de travail', valeur: 'Temps plein' },
    { label: 'Télétravail', valeur: 'Jusqu\'à 2 jours par semaine' },
  ],
  etapesProcessus: [
    'Étude du dossier de candidature',
    'Présélection téléphonique (20 min)',
    'Entretien avec l\'équipe (1h)',
    'Décision',
  ],
}

// --- Candidatures (espace connecté) ---

export type StatutEtape = 'fait' | 'en_cours' | 'a_venir'

export interface EtapeTimeline {
  id: string
  label: string
  statut: StatutEtape
  date?: string
}

export type TypeAction = 'message' | 'document' | 'entretien'

export interface ActionRequise {
  id: string
  candidatureId: string
  type: TypeAction
  label: string
  cta: string
}

export interface Candidature {
  id: string
  poste: string
  organisme: string
  dateEnvoi: string
  etapes: EtapeTimeline[]
  prochaineEtapeLabel: string | null
  prochaineDate: string | null
  delaiIndicatif: string | null
}

export const candidatures: Candidature[] = [
  {
    id: 'cand-innovation-numerique',
    poste: 'Chargé·e de mission innovation numérique',
    organisme: 'Ministère de la Transformation et de la Fonction Publiques',
    dateEnvoi: '12 septembre 2026',
    etapes: [
      { id: 'e1', label: 'Candidature envoyée', statut: 'fait', date: '12 septembre' },
      { id: 'e2', label: 'Candidature étudiée', statut: 'fait', date: '14 septembre' },
      { id: 'e3', label: 'Présélection', statut: 'fait', date: '16 septembre' },
      { id: 'e4', label: 'Entretien', statut: 'en_cours', date: '18 septembre' },
      { id: 'e5', label: 'Décision', statut: 'a_venir' },
    ],
    prochaineEtapeLabel: 'Entretien avec le recruteur',
    prochaineDate: '18 septembre',
    delaiIndicatif: null,
  },
  {
    id: 'cand-rh',
    poste: 'Responsable ressources humaines',
    organisme: 'Conseil départemental du Rhône',
    dateEnvoi: '3 septembre 2026',
    etapes: [
      { id: 'e1', label: 'Candidature envoyée', statut: 'fait', date: '3 septembre' },
      { id: 'e2', label: 'Candidature étudiée', statut: 'fait', date: '5 septembre' },
      { id: 'e3', label: 'Présélection', statut: 'en_cours' },
      { id: 'e4', label: 'Entretien', statut: 'a_venir' },
      { id: 'e5', label: 'Décision', statut: 'a_venir' },
    ],
    prochaineEtapeLabel: 'Un document est nécessaire pour poursuivre l\'examen de votre dossier',
    prochaineDate: null,
    delaiIndicatif: 'Réponse attendue sous 10 jours environ',
  },
  {
    id: 'cand-chef-projet-si',
    poste: 'Chef·fe de projet SI',
    organisme: 'Direction interministérielle du numérique',
    dateEnvoi: '28 août 2026',
    etapes: [
      { id: 'e1', label: 'Candidature envoyée', statut: 'fait', date: '28 août' },
      { id: 'e2', label: 'Candidature étudiée', statut: 'fait', date: '1 septembre' },
      { id: 'e3', label: 'Présélection', statut: 'fait', date: '4 septembre' },
      { id: 'e4', label: 'Entretien', statut: 'fait', date: '9 septembre' },
      { id: 'e5', label: 'Décision', statut: 'en_cours' },
    ],
    prochaineEtapeLabel: 'Le recruteur vous a envoyé un message',
    prochaineDate: null,
    delaiIndicatif: 'Décision attendue sous 5 jours environ',
  },
  {
    id: 'cand-instructeur',
    poste: 'Instructeur·rice administratif·ve',
    organisme: 'Préfecture de la Gironde',
    dateEnvoi: '8 septembre 2026',
    etapes: [
      { id: 'e1', label: 'Candidature envoyée', statut: 'fait', date: '8 septembre' },
      { id: 'e2', label: 'Candidature étudiée', statut: 'en_cours' },
      { id: 'e3', label: 'Présélection', statut: 'a_venir' },
      { id: 'e4', label: 'Entretien', statut: 'a_venir' },
      { id: 'e5', label: 'Décision', statut: 'a_venir' },
    ],
    prochaineEtapeLabel: 'Votre candidature est en cours d\'étude',
    prochaineDate: null,
    delaiIndicatif: 'Réponse attendue sous 15 jours environ',
  },
]

export const actionsRequises: ActionRequise[] = [
  {
    id: 'a1',
    candidatureId: 'cand-chef-projet-si',
    type: 'message',
    label: 'Répondre au recruteur — Chef·fe de projet SI',
    cta: 'Répondre',
  },
  {
    id: 'a2',
    candidatureId: 'cand-rh',
    type: 'document',
    label: 'Déposer un document — Responsable ressources humaines',
    cta: 'Ajouter le document',
  },
  {
    id: 'a3',
    candidatureId: 'cand-innovation-numerique',
    type: 'entretien',
    label: 'Confirmer un entretien — Chargé·e de mission innovation numérique',
    cta: 'Confirmer',
  },
]

// --- Conversations ---

export interface Message {
  id: string
  auteur: 'candidat' | 'recruteur'
  texte: string
  date: string
  lu: boolean
}

export interface Conversation {
  id: string
  candidatureId: string
  poste: string
  organisme: string
  recruteurNom: string
  messages: Message[]
}

export const conversations: Conversation[] = [
  {
    id: 'conv-chef-projet-si',
    candidatureId: 'cand-chef-projet-si',
    poste: 'Chef·fe de projet SI',
    organisme: 'Direction interministérielle du numérique',
    recruteurNom: 'Marc Delattre',
    messages: [
      {
        id: 'm1',
        auteur: 'recruteur',
        texte: 'Bonjour, nous avons été convaincus par votre entretien. Avant de finaliser notre décision, '
          + 'pourriez-vous nous préciser votre disponibilité pour une prise de poste ?',
        date: '9 septembre, 14h20',
        lu: false,
      },
    ],
  },
  {
    id: 'conv-innovation-numerique',
    candidatureId: 'cand-innovation-numerique',
    poste: 'Chargé·e de mission innovation numérique',
    organisme: 'Ministère de la Transformation et de la Fonction Publiques',
    recruteurNom: 'Sophie Nguyen',
    messages: [
      {
        id: 'm1',
        auteur: 'recruteur',
        texte: 'Bonjour, nous souhaiterions vous proposer un entretien le 18 septembre à 10h, en visioconférence. '
          + 'Cela vous convient-il ?',
        date: '16 septembre, 9h05',
        lu: true,
      },
      {
        id: 'm2',
        auteur: 'candidat',
        texte: 'Bonjour, oui cela me convient très bien. Je vous remercie.',
        date: '16 septembre, 11h30',
        lu: true,
      },
    ],
  },
  {
    id: 'conv-rh',
    candidatureId: 'cand-rh',
    poste: 'Responsable ressources humaines',
    organisme: 'Conseil départemental du Rhône',
    recruteurNom: 'Julie Ferrand',
    messages: [
      {
        id: 'm1',
        auteur: 'recruteur',
        texte: 'Bonjour, votre dossier avance bien. Il nous manque une pièce justificative pour poursuivre — '
          + 'vous la trouverez dans l\'onglet Documents de votre candidature.',
        date: '5 septembre, 16h45',
        lu: true,
      },
    ],
  },
]

// --- Documents ---

export type StatutDocument = 'fourni' | 'a_fournir'

export interface DocumentDemande {
  id: string
  candidatureId: string
  nom: string
  statut: StatutDocument
  obligatoire: boolean
  raison: string
  etape: string
  visiblePar: string
}

export const documents: DocumentDemande[] = [
  {
    id: 'd1',
    candidatureId: 'cand-rh',
    nom: 'CV',
    statut: 'fourni',
    obligatoire: true,
    raison: 'Déposé lors de l\'envoi de votre candidature',
    etape: 'Candidature',
    visiblePar: 'L\'équipe de recrutement du Conseil départemental du Rhône',
  },
  {
    id: 'd2',
    candidatureId: 'cand-rh',
    nom: 'Lettre de motivation',
    statut: 'fourni',
    obligatoire: false,
    raison: 'Déposée lors de l\'envoi de votre candidature',
    etape: 'Candidature',
    visiblePar: 'L\'équipe de recrutement du Conseil départemental du Rhône',
  },
  {
    id: 'd3',
    candidatureId: 'cand-rh',
    nom: 'Justificatif de titularisation',
    statut: 'a_fournir',
    obligatoire: true,
    raison: 'Nécessaire pour vérifier votre éligibilité au poste avant l\'entretien',
    etape: 'Présélection',
    visiblePar: 'L\'équipe de recrutement du Conseil départemental du Rhône',
  },
]

export function candidatureParId(id: string): Candidature | undefined {
  return candidatures.find(c => c.id === id)
}
