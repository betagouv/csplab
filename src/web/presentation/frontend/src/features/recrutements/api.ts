import type {
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
  RecrutementDetail,
} from './types'
import { api } from '@/api/client'

export async function getRecrutementDetail(
  organismeUuid: string,
  recrutementUuid: string,
): Promise<RecrutementDetail> {
  const { data } = await api.GET(
    '/recruteur/organisme/{organisme_uuid}/recrutements/{recrutement_uuid}',
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

export async function getRecrutementsActifs(organismeUuid: string): Promise<PaginatedRecrutementsActifsResponse> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements-actifs', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}

export async function getRecrutementsArchives(organismeUuid: string): Promise<PaginatedRecrutementsArchivesResponse> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements-archives', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}
