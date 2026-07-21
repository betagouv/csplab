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
