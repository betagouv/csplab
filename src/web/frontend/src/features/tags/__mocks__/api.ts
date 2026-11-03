import type * as Api from '@/features/tags/api'

export const getTags: typeof Api.getTags = async () => []

export const createTag: typeof Api.createTag = async (_organismeUuid, payload) => ({ uuid: crypto.randomUUID(), usage_count: 0, ...payload })

export const updateTag: typeof Api.updateTag = async (_organismeUuid, tagUuid, payload) => ({ uuid: tagUuid, category: 'candidature', usage_count: 0, ...payload })
