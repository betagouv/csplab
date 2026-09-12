import { defineQueryOptions } from '@pinia/colada'
import { getEquipeRecrutement } from './api'

export const EQUIPE_RECRUTEMENT_QUERY_KEYS = {
  root: ['equipe-recrutement'] as const,
  byRecrutement: (organismeUuid: string, recrutementUuid: string) =>
    [...EQUIPE_RECRUTEMENT_QUERY_KEYS.root, organismeUuid, recrutementUuid] as const,
}

export const equipeRecrutementQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: { organismeUuid: string, recrutementUuid: string }) => ({
    key: EQUIPE_RECRUTEMENT_QUERY_KEYS.byRecrutement(organismeUuid, recrutementUuid),
    query: () => getEquipeRecrutement(organismeUuid, recrutementUuid),
  }),
)
