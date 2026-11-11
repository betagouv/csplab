import type { CreateTagPayload, Tag, UpdateTagPayload } from './types'
import type { OrganismeParams, TagParams } from '@/api/params'
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

export async function updateTag(organismeUuid: string, tagUuid: string, payload: UpdateTagPayload): Promise<Tag> {
  const { data } = await api.PUT('/recruteur/organismes/{organisme_uuid}/parametres/tags/{tag_uuid}', {
    params: { path: { organisme_uuid: organismeUuid, tag_uuid: tagUuid } },
    body: payload,
  })
  return data!
}

export async function deleteTag({ organismeUuid, tagUuid }: TagParams): Promise<void> {
  await api.DELETE('/recruteur/organismes/{organisme_uuid}/parametres/tags/{tag_uuid}', {
    params: { path: { organisme_uuid: organismeUuid, tag_uuid: tagUuid } },
  })
}
