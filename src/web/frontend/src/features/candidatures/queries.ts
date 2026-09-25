import type { CandidatureParams } from './types'
import { defineQueryOptions } from '@pinia/colada'
import { getCandidatureDetail, getCandidatureDocuments, getCandidatureListe, getMotifsRefus, getRecrutementKanban } from './api'

export const CANDIDATURES_QUERY_KEYS = {
  root: ['candidatures'] as const,
  recrutement: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.root, organismeUuid, recrutementUuid] as const,
  kanban: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'kanban'] as const,
  liste: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'liste'] as const,
  detail: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidature', candidatureUuid, 'detail'] as const,
  motifsRefus: (organismeUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.root, organismeUuid, 'motifs-refus'] as const,
  documents: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidature', candidatureUuid, 'documents'] as const,
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

export const candidatureDetailQuery = defineQueryOptions(
  (candidature: CandidatureParams) => ({
    key: CANDIDATURES_QUERY_KEYS.detail(candidature),
    query: () => getCandidatureDetail(candidature),
  }),
)

export const motifsRefusQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: CANDIDATURES_QUERY_KEYS.motifsRefus(organismeUuid),
    query: () => getMotifsRefus(organismeUuid),
  }),
)

export const candidatureDocumentsQuery = defineQueryOptions(
  (candidature: CandidatureParams) => ({
    key: CANDIDATURES_QUERY_KEYS.documents(candidature),
    query: () => getCandidatureDocuments(candidature),
  }),
)
