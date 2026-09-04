import { defineQueryOptions } from '@pinia/colada'
import { getCandidatureListe, getRecrutementKanban } from './api'

export const CANDIDATURES_QUERY_KEYS = {
  root: ['candidatures'] as const,
  recrutement: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.root, organismeUuid, recrutementUuid] as const,
  kanban: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'kanban'] as const,
  liste: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'liste'] as const,
}

export interface CandidaturesQueryParams {
  organismeUuid: string
  recrutementUuid: string
}

export const recrutementKanbanQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: CandidaturesQueryParams) => ({
    key: CANDIDATURES_QUERY_KEYS.kanban(organismeUuid, recrutementUuid),
    query: () => getRecrutementKanban(organismeUuid, recrutementUuid),
  }),
)

export const candidatureListeQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: CandidaturesQueryParams) => ({
    key: CANDIDATURES_QUERY_KEYS.liste(organismeUuid, recrutementUuid),
    query: () => getCandidatureListe(organismeUuid, recrutementUuid),
  }),
)
