import type { CreateTagPayload, Tag } from './types'
import type { OrganismeParams } from '@/api/params'
import { api } from '@/api/client'

export async function getTags({ organismeUuid }: OrganismeParams): Promise<Tag[]> {
  const { data } = await api.GET('/recruteur/organismes/{organisme_uuid}/parametres/tags', {
    params: { path: { organisme_uuid: organismeUuid } },
  })
  return data!.results
}

export async function createTag(organismeUuid: string, payload: CreateTagPayload): Promise<Tag> {
  const { data } = await api.POST('/recruteur/organismes/{organisme_uuid}/parametres/tags', {
    params: { path: { organisme_uuid: organismeUuid } },
    body: payload,
  })
  return data!
}
