import type { OrganismeParams } from '@/api/params'
import { defineQueryOptions } from '@pinia/colada'
import { getOrganismeDetail } from '@/api/organismes'
import { organismeKeys } from '@/api/queryKeys'

export const organismeDetailQuery = defineQueryOptions((params: OrganismeParams) => {
  return {
    key: organismeKeys.detail(params),
    query: () => getOrganismeDetail(params),
  }
})
