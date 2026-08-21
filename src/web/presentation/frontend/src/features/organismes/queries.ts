import { defineQueryOptions } from '@pinia/colada'
import { getOrganismeAgents, getOrganismesList } from './api'

export const ORGANISMES_QUERY_KEYS = {
  root: ['organismes'] as const,
}

export const organismesListQuery = defineQueryOptions({
  key: [...ORGANISMES_QUERY_KEYS.root, 'list'],
  query: getOrganismesList,
})

export const organismeAgentsQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: [...ORGANISMES_QUERY_KEYS.root, organismeUuid, 'agents'] as const,
    query: () => getOrganismeAgents(organismeUuid),
  }),
)
