import type { OrganismesList } from './types'
import { api } from '@/api/client'

export async function getOrganismes(): Promise<OrganismesList[]> {
  const { data } = await api.GET('/recruteur/organismes')
  return data!
}
