import { defineQueryOptions } from '@pinia/colada'
import { getComptesUtilisateurs, getOrganismes } from './api'

export const ORGANISMES_QUERY_KEYS = {
  root: ['organismes'] as const,
}

export const organismesQuery = defineQueryOptions({
  key: ORGANISMES_QUERY_KEYS.root,
  query: getOrganismes,
})

export const comptesUtilisateursQuery = defineQueryOptions(
  ({ organismeUuid }: { organismeUuid: string }) => ({
    key: [...ORGANISMES_QUERY_KEYS.root, organismeUuid, 'comptes'] as const,
    query: () => getComptesUtilisateurs(organismeUuid),
  }),
)
