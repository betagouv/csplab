import { defineQueryOptions } from '@pinia/colada'
import { getOrganismesList } from './api'

export const ORGANISMES_QUERY_KEYS = {
  root: ['organismes'] as const,
}

export const organismesListQuery = defineQueryOptions({
  key: [...ORGANISMES_QUERY_KEYS.root, 'list'],
  query: getOrganismesList,
})
