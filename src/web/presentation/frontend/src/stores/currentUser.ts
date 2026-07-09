import type { Utilisateur } from '@/api/utilisateur'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getMe } from '@/api/utilisateur'

export const useCurrentUserStore = defineStore('currentUser', () => {
  const user = ref<Utilisateur | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  let fetchPromise: Promise<void> | null = null

  const displayName = computed(() =>
    user.value ? `${user.value.prenom} ${user.value.nom}` : '',
  )

  function fetch(): Promise<void> {
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

  return { user, loading, error, displayName, fetch }
})
