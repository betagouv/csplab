import type { Pinia } from 'pinia'
import type { Router } from 'vue-router'
import type { Utilisateur } from '@/api/utilisateur'
import { useQueryCache } from '@pinia/colada'
import { CURRENT_USER_QUERY_KEY, fetchCurrentUser } from '@/stores/currentUser'

declare module 'vue-router' {
  interface RouteMeta {
    requiresCurrentOrganisme?: boolean
  }
}

async function ensureCurrentUser(pinia: Pinia): Promise<Utilisateur> {
  const queryCache = useQueryCache(pinia)
  const cached = queryCache.getQueryData<Utilisateur>([...CURRENT_USER_QUERY_KEY])
  if (cached)
    return cached
  const user = await fetchCurrentUser()
  queryCache.setQueryData([...CURRENT_USER_QUERY_KEY], user)
  return user
}

export function registerNavigationGuards(router: Router, pinia: Pinia): void {
  router.beforeEach(async (to) => {
    if (!to.meta.requiresCurrentOrganisme)
      return true
    const user = await ensureCurrentUser(pinia)
    if (user.organisme_roles.length === 0)
      return { name: 'home' }
    return true
  })
}
