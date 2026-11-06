import type { RouteLocationRaw } from 'vue-router'
import type { Utilisateur } from '@/api/utilisateur'
import { loadCurrentUser } from '@/stores/currentUser'
import { can } from '@/utils/authorizedActions'
import { organismeHomeLocation, ORGANISMES_ROUTE_NAME } from './names'

export function homeLocationFor(user: Utilisateur | undefined): RouteLocationRaw | true {
  const organismeUuid = user?.organismes[0]?.uuid
  if (organismeUuid) {
    return organismeHomeLocation(organismeUuid)
  }
  return can(user?.authorized_actions, 'list_organismes') ? { name: ORGANISMES_ROUTE_NAME } : true
}

export async function redirectHome(): Promise<RouteLocationRaw | true> {
  const user = await loadCurrentUser().catch(() => undefined)
  return homeLocationFor(user)
}
