import type { CandidatureParams } from './types'
import { defineQueryOptions } from '@pinia/colada'
import { getCandidatureDetail, getCandidatureDocuments, getCandidatureNotes, getCandidatures, getMotifsRefus } from './api'

export const CANDIDATURES_QUERY_KEYS = {
  root: ['candidatures'] as const,
  recrutement: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.root, organismeUuid, recrutementUuid] as const,
  candidatures: (organismeUuid: string, recrutementUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidatures'] as const,
  detail: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidature', candidatureUuid, 'detail'] as const,
  motifsRefus: (organismeUuid: string) =>
    [...CANDIDATURES_QUERY_KEYS.root, organismeUuid, 'motifs-refus'] as const,
  documents: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidature', candidatureUuid, 'documents'] as const,
  notes: ({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) =>
    [...CANDIDATURES_QUERY_KEYS.recrutement(organismeUuid, recrutementUuid), 'candidature', candidatureUuid, 'notes'] as const,
}

export interface CandidaturesQueryParams {
  organismeUuid: string
  recrutementUuid: string
}

export const candidaturesQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: CandidaturesQueryParams) => ({
    key: CANDIDATURES_QUERY_KEYS.candidatures(organismeUuid, recrutementUuid),
    query: () => getCandidatures(organismeUuid, recrutementUuid),
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

export const candidatureNotesQuery = defineQueryOptions(
  (candidature: CandidatureParams) => ({
    key: CANDIDATURES_QUERY_KEYS.notes(candidature),
    query: () => getCandidatureNotes(candidature),
  }),
)
