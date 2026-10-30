import type { QueryCache } from '@pinia/colada'
import type { RecrutementParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { getEquipeRecrutement } from './api'

export const equipeRecrutementQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.equipe(params),
    query: () => getEquipeRecrutement(params),
  }
})

export function invalidateEquipeRecrutement(queryCache: QueryCache, params: RecrutementParams) {
  return Promise.all([
    queryCache.invalidateQueries({ key: recrutementKeys.equipe(params) }),
    queryCache.invalidateQueries({ key: organismeKeys.recrutementsActifs(params) }),
    queryCache.invalidateQueries({ key: organismeKeys.recrutementsArchives(params) }),
  ])
}
