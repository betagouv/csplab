import { defineQueryOptions } from '@pinia/colada'
import { getEtapesOffre, getEtapesRecrutement } from './api'

export const ETAPES_RECRUTEMENT_QUERY_KEYS = {
  root: ['etapes-recrutement'] as const,
  byOrganisme: (organismeUuid: string) =>
    [...ETAPES_RECRUTEMENT_QUERY_KEYS.root, organismeUuid] as const,
  byOffre: (organismeUuid: string, recrutementUuid: string) =>
    [...ETAPES_RECRUTEMENT_QUERY_KEYS.root, 'offre', organismeUuid, recrutementUuid] as const,
}

export const etapesRecrutementQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: ETAPES_RECRUTEMENT_QUERY_KEYS.byOrganisme(organismeUuid),
    query: () => getEtapesRecrutement(organismeUuid),
  }),
)

export const etapesOffreQuery = defineQueryOptions(
  ({ organismeUuid, recrutementUuid }: { organismeUuid: string, recrutementUuid: string }) => ({
    key: ETAPES_RECRUTEMENT_QUERY_KEYS.byOffre(organismeUuid, recrutementUuid),
    query: () => getEtapesOffre(organismeUuid, recrutementUuid),
  }),
)
