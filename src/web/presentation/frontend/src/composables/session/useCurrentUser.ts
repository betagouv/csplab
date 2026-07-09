import type { Utilisateur } from '@/api/utilisateur'
import { computed, readonly, ref } from 'vue'
import { getMe } from '@/api/utilisateur'

const user = ref<Utilisateur | null>(null)
const loading = ref(false)
const error = ref<Error | null>(null)

let fetchPromise: Promise<void> | null = null

async function fetchUser(): Promise<void> {
  if (fetchPromise)
    return fetchPromise

  loading.value = true
  error.value = null

  fetchPromise = getMe()
    .then((data) => {
      user.value = data
    })
    .catch((err) => {
      error.value = err
      user.value = null
    })
    .finally(() => {
      loading.value = false
      fetchPromise = null
    })

  return fetchPromise
}

const displayName = computed(() =>
  user.value ? `${user.value.prenom} ${user.value.nom}` : '',
)

export function useCurrentUser() {
  return {
    user: readonly(user),
    displayName: readonly(displayName),
    loading: readonly(loading),
    error: readonly(error),
    fetch: fetchUser,
  }
}
