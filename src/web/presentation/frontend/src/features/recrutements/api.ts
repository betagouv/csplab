import type { components } from '@/types/api'
import { api } from '@/api/client'

export type PaginatedRecrutementsActifsResponse = components['schemas']['PaginatedRecrutementsActifsResponse']
export type PaginatedRecrutementsArchivesResponse = components['schemas']['PaginatedRecrutementsArchivesResponse']
export type PaginatedRecrutements = PaginatedRecrutementsActifsResponse | PaginatedRecrutementsArchivesResponse

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
