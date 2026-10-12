import type { RecrutementParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { recrutementKeys } from '@/api/queryKeys'
import { getEquipeRecrutement } from './api'

export const equipeRecrutementQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.equipe(params),
    query: () => getEquipeRecrutement(params),
  }
})
