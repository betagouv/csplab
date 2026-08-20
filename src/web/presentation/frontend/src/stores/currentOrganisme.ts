import { computed } from 'vue'
import { useCurrentUser } from '@/stores/currentUser'

export function useCurrentOrganisme() {
  const { user } = useCurrentUser()

  const organisme = computed(() => {
    return user.value?.organisme_roles?.[0] ?? null
  })

  const organismeUuid = computed(() => organisme.value?.organisme_uuid ?? null)

  return {
    organisme,
    organismeUuid,
  }
}
