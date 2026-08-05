import type { useQueryCache } from '@pinia/colada'
import type {
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
} from './types'
import { defineQueryOptions } from '@pinia/colada'
import {
  getRecrutementDetail,
  getRecrutementsActifs,
  getRecrutementsArchives,
} from './api'

export const RECRUTEMENTS_QUERY_KEYS = {
  root: ['recrutements'] as const,
  actifs: (organismeUuid: string) =>
    [...RECRUTEMENTS_QUERY_KEYS.root, organismeUuid, 'actifs'] as const,
  archives: (organismeUuid: string) =>
    [...RECRUTEMENTS_QUERY_KEYS.root, organismeUuid, 'archives'] as const,
  detail: (organismeUuid: string, recrutementUuid: string) =>
    [...RECRUTEMENTS_QUERY_KEYS.root, organismeUuid, recrutementUuid] as const,
}

export const recrutementDetailQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: {
    organismeUuid: string
    recrutementUuid: string
  }) => ({
    key: RECRUTEMENTS_QUERY_KEYS.detail(organismeUuid, recrutementUuid),
    query: () => getRecrutementDetail(organismeUuid, recrutementUuid),
  }),
)

export const recrutementsActifsQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: RECRUTEMENTS_QUERY_KEYS.actifs(organismeUuid),
    query: () => getRecrutementsActifs(organismeUuid),
  }),
)

export const recrutementsArchivesQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: RECRUTEMENTS_QUERY_KEYS.archives(organismeUuid),
    query: () => getRecrutementsArchives(organismeUuid),
  }),
)

export function peekRecrutementIntitule(
  queryCache: ReturnType<typeof useQueryCache>,
  organismeUuid: string,
  offerId: string,
): string | null {
  const lists = [
    queryCache.getQueryData<PaginatedRecrutementsActifsResponse>(
      RECRUTEMENTS_QUERY_KEYS.actifs(organismeUuid),
    ),
    queryCache.getQueryData<PaginatedRecrutementsArchivesResponse>(
      RECRUTEMENTS_QUERY_KEYS.archives(organismeUuid),
    ),
  ]

  for (const list of lists) {
    const row = list?.results?.find(r => r.offer_id === offerId)
    if (row) {
      return row.intitule
    }
  }
  return null
}
