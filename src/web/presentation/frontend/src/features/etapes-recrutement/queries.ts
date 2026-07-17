import { defineQueryOptions } from '@pinia/colada'
import { getEtapesRecrutement } from './api'

export const ETAPES_RECRUTEMENT_QUERY_KEYS = {
  root: ['etapes-recrutement'] as const,
  byOrganisme: (organismeUuid: string) =>
    [...ETAPES_RECRUTEMENT_QUERY_KEYS.root, organismeUuid] as const,
}

export const etapesRecrutementQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: ETAPES_RECRUTEMENT_QUERY_KEYS.byOrganisme(organismeUuid),
    query: () => getEtapesRecrutement(organismeUuid),
  }),
)
