import { defineQueryOptions } from '@pinia/colada'
import { getOrganismes } from './api'

export const ORGANISMES_QUERY_KEYS = {
  root: ['organismes'] as const,
}

export const organismesQuery = defineQueryOptions({
  key: ORGANISMES_QUERY_KEYS.root,
  query: getOrganismes,
})
