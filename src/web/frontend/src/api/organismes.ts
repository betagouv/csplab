import type { OrganismeParams } from './params'
import type { components } from '@/types/api'
import { api } from './client'

export type OrganismeRead = components['schemas']['OrganismeRead']

export async function getOrganismeDetail({ organismeUuid }: OrganismeParams): Promise<OrganismeRead> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!
}
