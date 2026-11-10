import type { AuthorizedAction } from '@/utils/authorizedActions'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { canBrowseOrganismes as userCanBrowseOrganismes } from '@/api/utilisateur'
import { useCurrentUser } from '@/stores/currentUser'
import { organismeDetailQuery } from '@/stores/organismeDetail'
import { can } from '@/utils/authorizedActions'

export function useRouteOrganisme() {
  const route = useRoute()
  const { user } = useCurrentUser()

  const organismes = computed(() => user.value?.organismes ?? [])
  const canBrowseOrganismes = computed(() => userCanBrowseOrganismes(user.value))

  const routeOrganismeUuid = computed<string | null>(() => {
    const param = route.params.organismeUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const organismeUuid = computed<string | null>(() => {
    if (routeOrganismeUuid.value || canBrowseOrganismes.value) {
      return routeOrganismeUuid.value
    }
    return organismes.value[0]?.uuid ?? null
  })

  const organisme = computed(() =>
    organismes.value.find(o => o.uuid === organismeUuid.value) ?? null,
  )

  const readsNonMemberActions = computed(() =>
    canBrowseOrganismes.value && Boolean(organismeUuid.value) && !organisme.value,
  )

  const nonMemberOrganisme = useQuery(() => ({
    ...organismeDetailQuery({ organismeUuid: organismeUuid.value ?? '' }),
    enabled: readsNonMemberActions.value,
  }))

  const organismeActions = computed(() => organisme.value?.authorized_actions ?? nonMemberOrganisme.data.value?.authorized_actions)

  const actionsPending = computed(() => readsNonMemberActions.value && nonMemberOrganisme.isPending.value)

  function canOnOrganisme(action: AuthorizedAction): boolean {
    return can(organismeActions.value, action)
  }

  return {
    organismes,
    canBrowseOrganismes,
    routeOrganismeUuid,
    organismeUuid,
    organisme,
    actionsPending,
    nonMemberOrganisme: nonMemberOrganisme.data,
    canOnOrganisme,
  }
}
