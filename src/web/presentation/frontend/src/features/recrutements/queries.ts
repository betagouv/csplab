import type { useQueryCache } from '@pinia/colada'
import type {
  PaginatedRecrutementsActifsResponse,
  PaginatedRecrutementsArchivesResponse,
} from './types'
import { defineQueryOptions } from '@pinia/colada'
import { getRecrutementsActifs, getRecrutementsArchives } from './api'

export const RECRUTEMENTS_QUERY_KEYS = {
  root: ['recrutements'] as const,
  actifs: (organismeUuid: string) =>
    [...RECRUTEMENTS_QUERY_KEYS.root, organismeUuid, 'actifs'] as const,
  archives: (organismeUuid: string) =>
    [...RECRUTEMENTS_QUERY_KEYS.root, organismeUuid, 'archives'] as const,
}

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
