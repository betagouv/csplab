import type { PaginatedCandidatureListeList, RecrutementDetailKanban } from './types'
import { api } from '@/api/client'

export async function getRecrutementKanban(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<RecrutementDetailKanban> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/kanban',
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

export async function getCandidatureListe(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<PaginatedCandidatureListeList> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}/liste',
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
