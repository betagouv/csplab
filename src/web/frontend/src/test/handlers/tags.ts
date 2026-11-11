import type { CreateTagPayload, Tag, UpdateTagPayload } from '@/features/tags/types'
import { CREATED_TAG, TAGS, TO_RECALL } from '@/test/fixtures/tags'
import { failure, http } from './http'

const TAGS_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/tags'
const TAG_PATH = '/recruteur/organismes/{organisme_uuid}/parametres/tags/{tag_uuid}'

export function tags(results: Tag[] = TAGS) {
  return http.get(TAGS_PATH, ({ response }) => response(200).json({ count: results.length, results }))
}

export function tagCreation(
  tag: Tag = CREATED_TAG,
  onRequest?: (organismeUuid: string, payload: CreateTagPayload) => void,
) {
  return http.post(TAGS_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, await request.json())
    return response(201).json(tag)
  })
}

export function tagCreationFailure(status: number) {
  return http.post(TAGS_PATH, ({ response }) => response.untyped(failure(status)))
}

export function tagUpdate(
  tag: Tag = TO_RECALL,
  onRequest?: (organismeUuid: string, tagUuid: string, payload: UpdateTagPayload) => void,
) {
  return http.put(TAG_PATH, async ({ params, request, response }) => {
    onRequest?.(params.organisme_uuid, params.tag_uuid, await request.json())
    return response(200).json(tag)
  })
}

export function tagUpdateFailure(status: number) {
  return http.put(TAG_PATH, ({ response }) => response.untyped(failure(status)))
}

export function tagDeletion(onRequest?: (organismeUuid: string, tagUuid: string) => void) {
  return http.delete(TAG_PATH, ({ params, response }) => {
    onRequest?.(params.organisme_uuid, params.tag_uuid)
    return response(204).empty()
  })
}

export function tagDeletionFailure(status: number) {
  return http.delete(TAG_PATH, ({ response }) => response.untyped(failure(status)))
}

export const tagsHandlers = [
  tags(),
  tagCreation(),
  tagUpdate(),
  tagDeletion(),
]
