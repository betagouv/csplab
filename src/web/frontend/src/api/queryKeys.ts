import type { CandidatureParams, ConversationParams, DocumentParams, OrganismeParams, RecrutementParams } from './params'

export const organismeKeys = {
  all: ['organismes'] as const,
  list: () => {
    return [...organismeKeys.all, 'list'] as const
  },
  root: (params: OrganismeParams) => {
    return [...organismeKeys.all, params.organismeUuid] as const
  },
  detail: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'detail'] as const
  },
  agents: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'parametres', 'agents'] as const
  },
  etapes: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'parametres', 'etapes'] as const
  },
  motifsRefus: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'parametres', 'motifs-refus'] as const
  },
  recrutementsActifs: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'recrutements-actifs'] as const
  },
  recrutementsArchives: (params: OrganismeParams) => {
    return [...organismeKeys.root(params), 'recrutements-archives'] as const
  },
}

export const recrutementKeys = {
  root: (params: RecrutementParams) => {
    return [...organismeKeys.root(params), 'recrutements', params.recrutementUuid] as const
  },
  detail: (params: RecrutementParams) => {
    return [...recrutementKeys.root(params), 'detail'] as const
  },
  etapes: (params: RecrutementParams) => {
    return [...recrutementKeys.root(params), 'etapes'] as const
  },
  equipe: (params: RecrutementParams) => {
    return [...recrutementKeys.root(params), 'parametres', 'agents'] as const
  },
  kanban: (params: RecrutementParams) => {
    return [...recrutementKeys.root(params), 'kanban'] as const
  },
  liste: (params: RecrutementParams) => {
    return [...recrutementKeys.root(params), 'liste'] as const
  },
}

export const candidatureKeys = {
  root: (params: CandidatureParams) => {
    return [...recrutementKeys.root(params), 'candidatures', params.candidatureUuid] as const
  },
  detail: (params: CandidatureParams) => {
    return [...candidatureKeys.root(params), 'detail'] as const
  },
  documents: (params: CandidatureParams) => {
    return [...candidatureKeys.root(params), 'documents'] as const
  },
  document: (params: DocumentParams) => {
    return [...candidatureKeys.documents(params), params.documentUuid] as const
  },
  notes: (params: CandidatureParams) => {
    return [...candidatureKeys.root(params), 'notes'] as const
  },
  activites: (params: CandidatureParams) => {
    return [...candidatureKeys.root(params), 'logs'] as const
  },
  activitesList: (params: CandidatureParams & { limit?: number }) => {
    return [...candidatureKeys.activites(params), params.limit ?? null] as const
  },
  conversations: (params: CandidatureParams) => {
    return [...candidatureKeys.root(params), 'conversations'] as const
  },
  conversation: (params: ConversationParams) => {
    return [...candidatureKeys.conversations(params), params.conversationUuid] as const
  },
}
