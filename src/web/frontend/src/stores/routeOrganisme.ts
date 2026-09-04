import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrentUser } from '@/stores/currentUser'

export function useRouteOrganisme() {
  const route = useRoute()
  const { user } = useCurrentUser()

  const organismes = computed(() => user.value?.organisme_roles ?? [])

  const routeOrganismeUuid = computed<string | null>(() => {
    const param = route.params.organismeUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const organismeUuid = computed<string | null>(() =>
    routeOrganismeUuid.value ?? organismes.value[0]?.organisme_uuid ?? null,
  )

  const organisme = computed(() =>
    organismes.value.find(o => o.organisme_uuid === organismeUuid.value) ?? null,
  )

  const canManageOrganisme = computed(() =>
    Boolean(user.value?.is_staff) || organisme.value?.role === 'responsable',
  )

  return {
    organismes,
    routeOrganismeUuid,
    organismeUuid,
    organisme,
    canManageOrganisme,
  }
}
