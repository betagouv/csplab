import type { OrganismeParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { organismeKeys } from '@/api/queryKeys'
import { getTags } from './api'

export const tagsQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.tags(params),
    query: () => getTags(params),
  }
})
