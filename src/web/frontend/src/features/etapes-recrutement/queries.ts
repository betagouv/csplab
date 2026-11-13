import type { OrganismeParams, RecrutementParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { getEtapesOffre, getEtapesRecrutement, initEtapesRecrutement } from './api'

export const etapesRecrutementQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.etapes(params),
    query: async () => {
      const etapes = await getEtapesRecrutement(params)
      return etapes.length > 0 ? etapes : initEtapesRecrutement(params)
    },
  }
})

export const etapesOffreQuery = defineQueryOptions((params: RecrutementParams) => {
  return {
    key: recrutementKeys.etapes(params),
    query: () => getEtapesOffre(params),
  }
})
