import type { CreateOrganismePayload, OrganismeDetail, OrganismesList } from './types'
import { api } from '@/api/client'

export async function getOrganismesList(): Promise<OrganismesList[]> {
  const { data } = await api.GET('/recruteur/organismes')
  return data!
}

export async function createOrganisme(payload: CreateOrganismePayload): Promise<OrganismeDetail> {
  const { data } = await api.POST('/recruteur/organismes', { body: payload })
  return data!
}
