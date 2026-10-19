import type { ActivitesParams } from './types'
import type { CandidatureParams, DocumentParams, OrganismeParams, RecrutementParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { candidatureKeys, organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { checkCandidatureDocument, getCandidatureActivites, getCandidatureDetail, getCandidatureDocuments, getCandidatureListe, getCandidatureNotes, getMotifsRefus, getRecrutementKanban } from './api'

export const recrutementKanbanQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.kanban(params),
    query: () => getRecrutementKanban(params),
  }
})

export const candidatureListeQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.liste(params),
    query: () => getCandidatureListe(params),
  }
})

export const candidatureDetailQuery = defineQueryOptions((params: CandidatureParams) => {
  return {
    key: candidatureKeys.detail(params),
    query: () => getCandidatureDetail(params),
  }
})

export const motifsRefusQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.motifsRefus(params),
    query: () => getMotifsRefus(params),
  }
})

export const candidatureDocumentsQuery = defineQueryOptions((params: CandidatureParams) => {
  return {
    key: candidatureKeys.documents(params),
    query: () => getCandidatureDocuments(params),
  }
})

export const candidatureNotesQuery = defineQueryOptions((params: CandidatureParams) => {
  return {
    key: candidatureKeys.notes(params),
    query: () => getCandidatureNotes(params),
  }
})

export const candidatureDocumentCheckQuery = defineQueryOptions((params: DocumentParams) => {
  return {
    key: candidatureKeys.document(params),
    query: () => checkCandidatureDocument(params),
  }
})

export const candidatureActivitesQuery = defineQueryOptions((params: ActivitesParams) => {
  return {
    key: candidatureKeys.activitesList(params),
    query: () => getCandidatureActivites(params),
  }
})
