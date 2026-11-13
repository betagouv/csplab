import type { QueryCache } from '@pinia/colada'
import type { OrganismeParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { getOrganismeAgents, getOrganismesList, searchOrganismes } from './api'

export const organismesListQuery = defineQueryOptions({
  key: organismeKeys.list(),
  query: getOrganismesList,
})

export const organismesSearchQuery = defineQueryOptions((nom: string) => {
  return {
    key: organismeKeys.search(nom),
    query: () => searchOrganismes(nom),
  }
})

export const organismeAgentsQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.agents(params),
    query: () => getOrganismeAgents(params),
  }
})

export function invalidateOrganisme(queryCache: QueryCache, params: OrganismeParams) {
  return Promise.all([
    queryCache.invalidateQueries({ key: organismeKeys.list() }),
    queryCache.invalidateQueries({ key: organismeKeys.detail(params) }),
    queryCache.invalidateQueries({ key: organismeKeys.agents(params) }),
  ])
}
