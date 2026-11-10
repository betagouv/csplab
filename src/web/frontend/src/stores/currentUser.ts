import type { Utilisateur } from '@/api/utilisateur'
import { defineQueryOptions, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { getMe } from '@/api/utilisateur'

export const CURRENT_USER_QUERY_KEY = ['currentUser'] as const

const currentUserQuery = defineQueryOptions({
  key: CURRENT_USER_QUERY_KEY,
  query: getMe,
  staleTime: Infinity,
})

export async function loadCurrentUser(): Promise<Utilisateur | undefined> {
  const queryCache = useQueryCache()
  const { data } = await queryCache.refresh(queryCache.ensure(currentUserQuery))
  return data
}

export function useCurrentUser() {
  const query = useQuery(currentUserQuery)

  const user = computed(() => query.data.value ?? null)
  const isStaff = computed(() => user.value?.is_staff ?? false)
  const displayName = computed(() =>
    user.value ? `${user.value.prenom} ${user.value.nom}` : '',
  )

  return {
    user,
    isStaff,
    displayName,
    status: query.status,
    isPending: query.isPending,
    error: query.error,
    refetch: query.refetch,
  }
}
