import type { QueryCache } from '@pinia/colada'
import type { OrganismesPageParams } from './types'
import type { OrganismeParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { getOrganismeAgents, getOrganismeDetail, getOrganismesPage, searchOrganismes } from './api'

export const organismesPageQuery = defineQueryOptions((params: OrganismesPageParams) => {
  return {
    key: organismeKeys.listPage(params),
    query: () => getOrganismesPage(params),
    placeholderData: previous => previous,
  }
})

export const organismesSearchQuery = defineQueryOptions((nom: string) => {
  return {
    key: organismeKeys.search(nom),
    query: () => searchOrganismes(nom),
  }
})

export const organismeDetailQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.detail(params),
    query: () => getOrganismeDetail(params),
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
