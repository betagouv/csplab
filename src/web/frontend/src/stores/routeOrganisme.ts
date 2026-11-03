import type { AuthorizedAction } from '@/utils/authorizedActions'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrentUser } from '@/stores/currentUser'
import { can } from '@/utils/authorizedActions'

export function useRouteOrganisme() {
  const route = useRoute()
  const { user, isStaff } = useCurrentUser()

  const organismes = computed(() => user.value?.organisme_roles ?? [])

  const routeOrganismeUuid = computed<string | null>(() => {
    const param = route.params.organismeUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const organismeUuid = computed<string | null>(() => {
    if (routeOrganismeUuid.value || isStaff.value) {
      return routeOrganismeUuid.value
    }
    return organismes.value[0]?.organisme_uuid ?? null
  })

  const organisme = computed(() =>
    organismes.value.find(o => o.organisme_uuid === organismeUuid.value) ?? null,
  )

  const canManageOrganisme = computed(() =>
    isStaff.value || organisme.value?.role === 'superviseur',
  )

  const organismeActions = computed(() =>
    user.value?.organismes.find(o => o.uuid === organismeUuid.value)?.authorized_actions,
  )

  function canOnOrganisme(action: AuthorizedAction): boolean {
    return isStaff.value || can(organismeActions.value, action)
  }

  return {
    organismes,
    routeOrganismeUuid,
    organismeUuid,
    organisme,
    canManageOrganisme,
    canOnOrganisme,
  }
}
