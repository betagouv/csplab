import type * as Api from '@/features/candidatures/api'
import { paginated } from '@/api/__mocks__/demo'
import { HttpError } from '@/api/errors'
import demoCvUrl from '@/features/candidatures/__mocks__/cv-demo.pdf?url'
import {
  addDemoNote,
  DEMO_MOTIFS_REFUS,
  demoActivites,
  demoCandidatureDetail,
  demoDocuments,
  demoKanban,
  demoListe,
  demoNotes,
  moveDemoCandidatures,
} from '@/features/candidatures/__mocks__/demo'

export const getRecrutementKanban: typeof Api.getRecrutementKanban = async () => demoKanban()

export const getCandidatureDetail: typeof Api.getCandidatureDetail = async ({ candidatureUuid }) => {
  const detail = demoCandidatureDetail(candidatureUuid)
  if (!detail) {
    throw new HttpError(404, 'Not Found')
  }
  return detail
}

export const getCandidatureListe: typeof Api.getCandidatureListe = async () => paginated(demoListe())

export const patchEtapeCandidatures: typeof Api.patchEtapeCandidatures = async (_organismeUuid, _recrutementUuid, { etapeCibleUuid, candidatureUuids }) => {
  moveDemoCandidatures(candidatureUuids, etapeCibleUuid)
  return { reussites: candidatureUuids, echecs: [] }
}

export const getMotifsRefus: typeof Api.getMotifsRefus = async () => DEMO_MOTIFS_REFUS

export const getCandidatureDocuments: typeof Api.getCandidatureDocuments = async ({ candidatureUuid }) => paginated(demoDocuments(candidatureUuid))

export const checkCandidatureDocument: typeof Api.checkCandidatureDocument = async () => undefined

export const candidatureDocumentUrl: typeof Api.candidatureDocumentUrl = () => demoCvUrl

export const getCandidatureNotes: typeof Api.getCandidatureNotes = async ({ candidatureUuid }) => paginated(demoNotes(candidatureUuid))

export const createCandidatureNote: typeof Api.createCandidatureNote = async ({ candidatureUuid }, message) => {
  addDemoNote(candidatureUuid, message)
}

export const getCandidatureActivites: typeof Api.getCandidatureActivites = async ({ candidatureUuid, limit }) => {
  const activites = demoActivites(candidatureUuid)
  return { ...paginated(activites.slice(0, limit)), count: activites.length }
}
