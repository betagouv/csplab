import type * as Api from '@/features/agents/api'

const JULIEN_MOREAU = {
  uuid: 'e0000000-0000-4000-8000-000000000002',
  email: 'julien.moreau@example.gouv.fr',
  prenom: 'Julien',
  nom: 'Moreau',
  intitule_poste: 'Chargé de recrutement',
}

export const searchAgentByEmail: typeof Api.searchAgentByEmail = async () => JULIEN_MOREAU

export const createAgent: typeof Api.createAgent = async payload => ({ ...JULIEN_MOREAU, ...payload })
