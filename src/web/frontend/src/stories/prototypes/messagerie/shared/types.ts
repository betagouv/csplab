export type PersonId = 'camille' | 'jean-marc' | 'sophie' | 'karim'

export interface Person {
  id: PersonId
  prenom: string
  nom: string
  role: string
  fonction?: string
  equipe: boolean
}

export type Block
  = | { type: 'p', text: string }
    | { type: 'ul', items: string[] }

export interface MessageDocument {
  nom: string
  taille: number
}

export interface Slot {
  id: string
  start: string
}

export interface SlotRequest {
  slots: Slot[]
  deadline: string
  chosenSlotId?: string
  chosenAt?: string
}

export interface Message {
  id: string
  conversationId: string
  authorId: PersonId
  createdAt: string
  content: Block[]
  documents: MessageDocument[]
  readByCandidateAt?: string
  readByTeam: Partial<Record<PersonId, string>>
  awaitsReply?: boolean
  slotRequest?: SlotRequest
}

export interface Conversation {
  id: string
  objet: string
  createdBy: PersonId
  createdAt: string
}

export type Presentation = 'bulles' | 'pile' | 'correspondance'
export type SideRule = 'equipe' | 'moi'
export type Preset = 'immediat' | 'differe'
export type Order = 'chronologique' | 'recent-en-haut'

export interface Settings {
  presentation: Presentation
  sideRule: SideRule
  composer: 'ouverte' | 'bouton'
  dates: 'relatives' | 'absolues'
  readReceipts: boolean
  waitingLine: boolean
  order: Order
  progress: boolean
  indicativeDelay: boolean
}

export type Waiting
  = | { kind: 'equipe', since: string }
    | { kind: 'candidat', since: string, deadline?: string }
