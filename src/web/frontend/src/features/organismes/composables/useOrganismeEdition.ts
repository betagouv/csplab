import type { InjectionKey } from 'vue'
import type { OrganismesList } from '../types'
import type { Request } from '@/composables/ui/useRequest'
import { inject, provide } from 'vue'
import { createRequest } from '@/composables/ui/useRequest'

const KEY: InjectionKey<Request<OrganismesList>> = Symbol('organisme-edition')

export function provideOrganismeEdition(): Request<OrganismesList> {
  const edition = createRequest<OrganismesList>()
  provide(KEY, edition)
  return edition
}

export function useOrganismeEdition(): Request<OrganismesList> {
  const edition = inject(KEY)
  if (!edition)
    throw new Error('useOrganismeEdition must be used within provideOrganismeEdition')
  return edition
}
