import type { components } from '@/types/api'
import { api } from '@/utils/api'

export type PaginatedRecrutements = components['schemas']['PaginatedRecrutementsResponse']

export interface RecrutementsQuery {
  filtre?: 'actifs' | 'archives'
  page?: number
  size?: number
}

export async function getRecrutements(
  organismeUuid: string,
  query: RecrutementsQuery = {},
): Promise<PaginatedRecrutements> {
  const { data } = await api.GET('/recruteur/organisme/{organisme_uuid}/recrutements', {
    params: { path: { organisme_uuid: organismeUuid }, query },
  })
  return data!
}
