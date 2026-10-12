import type { QueryCache } from '@pinia/colada'
import type {
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
} from './types'
import type { OrganismeParams, RecrutementParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys, recrutementKeys } from '@/api/queryKeys'
import {
  getRecrutementDetail,
  getRecrutementsActifs,
  getRecrutementsArchives,
} from './api'

export const recrutementDetailQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.detail(params),
    query: () => getRecrutementDetail(params),
  }
})

export const recrutementsActifsQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.recrutementsActifs(params),
    query: () => getRecrutementsActifs(params),
  }
})

export const recrutementsArchivesQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.recrutementsArchives(params),
    query: () => getRecrutementsArchives(params),
  }
})

export function peekRecrutementIntitule(
  queryCache: QueryCache,
  organismeUuid: string,
  offerId: string,
): string | null {
  const lists = [
    queryCache.getQueryData<PaginatedRecrutementsActifsResponse>(
      organismeKeys.recrutementsActifs({ organismeUuid }),
    ),
    queryCache.getQueryData<PaginatedRecrutementsArchivesResponse>(
      organismeKeys.recrutementsArchives({ organismeUuid }),
    ),
  ]

  for (const list of lists) {
    const row = list?.results?.find(r => r.uuid === offerId)
    if (row) {
      return row.intitule
    }
  }
  return null
}
