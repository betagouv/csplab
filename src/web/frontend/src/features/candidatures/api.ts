import type { CandidatureDetail, CandidatureParams, ChangerEtapeResultat, MotifRefus, MotifRefusOption, PaginatedCandidatureListeList, PaginatedDocumentListeList, RecrutementDetailKanban } from './types'
import { api } from '@/api/client'

export async function getRecrutementKanban(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<RecrutementDetailKanban> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/kanban',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!
}

export async function getCandidatureDetail(candidature: CandidatureParams): Promise<CandidatureDetail> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}',
    { params: { path: candidaturePath(candidature) } },
  )
  return data!
}

export async function getCandidatureListe(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<PaginatedCandidatureListeList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/liste',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!
}

export interface EtapeChange {
  etapeCibleUuid: string
  candidatureUuids: string[]
  motifRefus?: MotifRefus
}

export async function patchEtapeCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
  { etapeCibleUuid, candidatureUuids, motifRefus }: EtapeChange,
): Promise<ChangerEtapeResultat> {
  const { data } = await api.PATCH(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/etape',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: {
        etape_cible_uuid: etapeCibleUuid,
        candidatures: candidatureUuids.map(uuid => ({ candidature_uuid: uuid })),
        motif_refus: motifRefus,
      },
    },
  )
  return data!
}

export async function getMotifsRefus(organismeUuid: string): Promise<MotifRefusOption[]> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/parametres/motifs-refus',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
        },
      },
    },
  )
  return data as MotifRefusOption[]
}

function candidaturePath({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) {
  return {
    organisme_uuid: organismeUuid,
    recrutement_uuid: recrutementUuid,
    candidature_uuid: candidatureUuid,
  }
}

export async function getCandidatureDocuments(candidature: CandidatureParams): Promise<PaginatedDocumentListeList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents',
    { params: { path: candidaturePath(candidature) } },
  )
  return data!
}

export function candidatureDocumentUrl(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
  documentUuid: string,
): string {
  return `/recruteur/organismes/${organismeUuid}/recrutements/${recrutementUuid}/candidatures/${candidatureUuid}/documents/${documentUuid}`
}
