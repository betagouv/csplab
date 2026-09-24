import type { Conversation, Message, Person, PersonId } from '../shared/types'

export const PEOPLE: Record<PersonId, Person> = {
  'camille': { id: 'camille', prenom: 'Camille', nom: 'Dupont', role: 'Candidate', equipe: false },
  'jean-marc': {
    id: 'jean-marc',
    prenom: 'Jean-Marc',
    nom: 'Chateau',
    role: 'Responsable',
    fonction: 'Chef du bureau de la communication',
    equipe: true,
  },
  'sophie': {
    id: 'sophie',
    prenom: 'Sophie',
    nom: 'Nguyen',
    role: 'Recruteuse',
    fonction: 'Gestionnaire RH',
    equipe: true,
  },
  'karim': {
    id: 'karim',
    prenom: 'Karim',
    nom: 'Benali',
    role: 'Contributeur',
    fonction: 'Membre du jury',
    equipe: true,
  },
}

export const CANDIDATURE = {
  offre: 'Chargé·e de communication',
  service: 'Direction de la communication',
  soumiseLe: '2026-09-01T10:04:00',
  etape: 'Entretien',
  etapes: ['Candidature envoyée', 'Examen du dossier', 'Entretien', 'Décision'],
  etapeIndex: 2,
  position: 1,
  total: 4,
}

export const TABS = [
  { value: 'candidature', label: 'Candidature', icon: 'ri:user-line' },
  { value: 'historique', label: 'Historique d’activité', icon: 'ri:time-line' },
  { value: 'documents', label: 'Documents', icon: 'ri:file-list-line' },
  { value: 'notes', label: 'Notes', icon: 'ri:sticky-note-line' },
  { value: 'messages', label: 'Messages', icon: 'ri:chat-3-line' },
]

export const NOW = '2026-09-25T16:00:00'
export const NOW_BEFORE_SLOT_CHOICE = '2026-09-22T14:00:00'

const TEAM_READ = (at: string): Message['readByTeam'] => ({ 'jean-marc': at, 'sophie': at, 'karim': at })

const PIECES: Conversation = {
  id: 'pieces',
  objet: 'Pièces complémentaires',
  createdBy: 'sophie',
  createdAt: '2026-09-03T09:12:00',
}

const ENTRETIEN: Conversation = {
  id: 'entretien',
  objet: 'Organisation de l’entretien',
  createdBy: 'jean-marc',
  createdAt: '2026-09-22T11:20:00',
}

const PIECES_MESSAGES: Message[] = [
  {
    id: 'pieces-1',
    conversationId: 'pieces',
    authorId: 'sophie',
    createdAt: '2026-09-03T09:12:00',
    readByCandidateAt: '2026-09-03T12:40:00',
    readByTeam: {},
    awaitsReply: true,
    documents: [],
    content: [
      { type: 'p', text: 'Bonjour Madame Dupont,' },
      { type: 'p', text: 'Nous avons bien reçu votre candidature au poste de chargé·e de communication et nous vous en remercions.' },
      { type: 'p', text: 'Afin de compléter votre dossier avant son examen par le jury, pourriez-vous nous transmettre les documents suivants :' },
      {
        type: 'ul',
        items: [
          'votre dernier contrat de travail ou votre dernier arrêté de nomination ;',
          'vos deux derniers comptes rendus d’entretien professionnel ;',
          'la copie de votre diplôme le plus élevé.',
        ],
      },
      { type: 'p', text: 'Vous pouvez les joindre en réponse à ce message, avant le vendredi 11 septembre.' },
      { type: 'p', text: 'Bien cordialement,\nSophie Nguyen\nGestionnaire RH, bureau du recrutement' },
    ],
  },
  {
    id: 'pieces-2',
    conversationId: 'pieces',
    authorId: 'camille',
    createdAt: '2026-09-06T21:47:00',
    readByTeam: TEAM_READ('2026-09-07T08:55:00'),
    documents: [
      { nom: 'master-communication-publique.pdf', taille: 1_240_000 },
      { nom: 'contrat-de-travail-2023.pdf', taille: 386_000 },
    ],
    content: [
      { type: 'p', text: 'Bonjour,' },
      { type: 'p', text: 'Veuillez trouver ci-joint mon diplôme et mon dernier contrat de travail. Je dois demander mes comptes rendus d’entretien professionnel à mon employeur actuel ; je vous les transmets dès que je les reçois.' },
      { type: 'p', text: 'Bien cordialement,\nCamille Dupont' },
    ],
  },
  {
    id: 'pieces-3',
    conversationId: 'pieces',
    authorId: 'sophie',
    createdAt: '2026-09-11T14:30:00',
    readByCandidateAt: '2026-09-11T18:03:00',
    readByTeam: {},
    awaitsReply: true,
    documents: [],
    content: [
      { type: 'p', text: 'Bonjour Madame Dupont,' },
      { type: 'p', text: 'Merci pour ces documents. Nous restons dans l’attente de vos deux derniers comptes rendus d’entretien professionnel, nécessaires à l’examen de votre candidature par le jury du 21 septembre.' },
      { type: 'p', text: 'Pourriez-vous nous les transmettre d’ici le vendredi 18 septembre ?' },
      { type: 'p', text: 'Bien cordialement,\nSophie Nguyen' },
    ],
  },
  {
    id: 'pieces-4',
    conversationId: 'pieces',
    authorId: 'camille',
    createdAt: '2026-09-14T08:05:00',
    readByTeam: TEAM_READ('2026-09-14T09:20:00'),
    documents: [
      { nom: 'compte-rendu-entretien-2024.pdf', taille: 412_000 },
      { nom: 'compte-rendu-entretien-2025.pdf', taille: 398_000 },
    ],
    content: [
      { type: 'p', text: 'Bonjour,' },
      { type: 'p', text: 'Voici mes deux comptes rendus d’entretien professionnel.' },
      { type: 'p', text: 'Bonne journée,\nCamille Dupont' },
    ],
  },
  {
    id: 'pieces-5',
    conversationId: 'pieces',
    authorId: 'sophie',
    createdAt: '2026-09-15T16:40:00',
    readByCandidateAt: '2026-09-15T19:02:00',
    readByTeam: {},
    documents: [],
    content: [
      { type: 'p', text: 'Bonjour Madame Dupont,' },
      { type: 'p', text: 'Votre dossier est complet. Il sera examiné par le jury le lundi 21 septembre ; nous reviendrons vers vous à l’issue de cet examen.' },
      { type: 'p', text: 'Bien cordialement,\nSophie Nguyen' },
    ],
  },
]

const INVITATION_OPENING = [
  { type: 'p', text: 'Bonjour Madame Dupont,' },
  { type: 'p', text: 'À la suite de l’examen de votre dossier par le jury, nous souhaitons vous rencontrer en entretien pour le poste de chargé·e de communication.' },
] satisfies Message['content']

const INVITATION_CLOSING = [
  { type: 'p', text: 'L’entretien dure 45 minutes, en présence de deux membres du jury.' },
  { type: 'p', text: 'Bien cordialement,\nJean-Marc Chateau\nChef du bureau de la communication' },
] satisfies Message['content']

const SLOTS = [
  { id: 'mardi-matin', start: '2026-09-29T09:30:00' },
  { id: 'mardi-apres-midi', start: '2026-09-29T14:00:00' },
  { id: 'jeudi-matin', start: '2026-10-01T10:30:00' },
]

function invitation(structured: boolean): Message {
  return {
    id: 'entretien-1',
    conversationId: 'entretien',
    authorId: 'jean-marc',
    createdAt: '2026-09-22T11:20:00',
    readByCandidateAt: '2026-09-22T12:04:00',
    readByTeam: {},
    awaitsReply: true,
    documents: [],
    content: structured
      ? [
          ...INVITATION_OPENING,
          { type: 'p', text: 'Merci de choisir ci-dessous le créneau qui vous convient.' },
          ...INVITATION_CLOSING,
        ]
      : [
          ...INVITATION_OPENING,
          { type: 'p', text: 'Nous vous proposons les créneaux suivants :' },
          {
            type: 'ul',
            items: ['mardi 29 septembre à 9 h 30 ;', 'mardi 29 septembre à 14 h ;', 'jeudi 1er octobre à 10 h 30.'],
          },
          { type: 'p', text: 'Merci de nous indiquer celui qui vous convient.' },
          ...INVITATION_CLOSING,
        ],
    slotRequest: structured
      ? { slots: SLOTS, deadline: '2026-09-25T18:00:00' }
      : undefined,
  }
}

const SLOT_REPLY: Message = {
  id: 'entretien-2',
  conversationId: 'entretien',
  authorId: 'camille',
  createdAt: '2026-09-22T12:15:00',
  readByTeam: TEAM_READ('2026-09-22T14:02:00'),
  documents: [],
  content: [
    { type: 'p', text: 'Bonjour,' },
    { type: 'p', text: 'Merci pour votre message. Le créneau du mardi 29 septembre à 14 h me convient parfaitement.' },
    { type: 'p', text: 'Je vous remercie et reste disponible si vous avez besoin d’informations complémentaires.' },
    { type: 'p', text: 'Bien cordialement,\nCamille Dupont' },
  ],
}

const CONVOCATION: Message = {
  id: 'entretien-3',
  conversationId: 'entretien',
  authorId: 'sophie',
  createdAt: '2026-09-23T09:30:00',
  readByCandidateAt: '2026-09-23T17:55:00',
  readByTeam: {},
  documents: [{ nom: 'convocation-entretien-29-septembre.pdf', taille: 208_000 }],
  content: [
    { type: 'p', text: 'Bonjour Madame Dupont,' },
    { type: 'p', text: 'Nous vous confirmons votre entretien le mardi 29 septembre à 14 h, au 14 rue du Bac, 75007 Paris, bâtiment B, 3e étage. Vous trouverez ci-joint votre convocation.' },
    { type: 'p', text: 'Merci de vous munir d’une pièce d’identité.' },
    { type: 'p', text: 'Bien cordialement,\nSophie Nguyen\nGestionnaire RH, bureau du recrutement' },
  ],
}

const REMOTE_QUESTION: Message = {
  id: 'entretien-4',
  conversationId: 'entretien',
  authorId: 'camille',
  createdAt: '2026-09-23T18:20:00',
  readByTeam: { 'jean-marc': '2026-09-24T09:10:00', 'sophie': '2026-09-24T08:40:00' },
  documents: [],
  content: [
    { type: 'p', text: 'Bonjour,' },
    { type: 'p', text: 'Merci pour la convocation. Serait-il possible de passer cet entretien en visioconférence ? J’habite à Lyon et le déplacement me demanderait de poser une journée de congé.' },
    { type: 'p', text: 'Bien cordialement,\nCamille Dupont' },
  ],
}

export type ScenarioKey = 'principal' | 'creneau-en-attente' | 'creneau-retenu'

export interface Scenario {
  now: string
  conversations: Conversation[]
  messages: Message[]
}

export function buildScenario(key: ScenarioKey): Scenario {
  if (key === 'principal') {
    return structuredClone({
      now: NOW,
      conversations: [ENTRETIEN, PIECES],
      messages: [...PIECES_MESSAGES, invitation(false), SLOT_REPLY, CONVOCATION, REMOTE_QUESTION],
    })
  }
  const structured = invitation(true)
  if (key === 'creneau-retenu' && structured.slotRequest) {
    structured.slotRequest.chosenSlotId = 'mardi-apres-midi'
    structured.slotRequest.chosenAt = '2026-09-22T12:15:00'
    structured.awaitsReply = false
  }
  return structuredClone({
    now: NOW_BEFORE_SLOT_CHOICE,
    conversations: [ENTRETIEN, PIECES],
    messages: [...PIECES_MESSAGES, structured],
  })
}
