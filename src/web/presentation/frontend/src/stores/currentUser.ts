import type { Utilisateur } from '@/api/utilisateur'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { getMe } from '@/api/utilisateur'

export const CURRENT_USER_QUERY_KEY = ['currentUser'] as const

export function useCurrentUser() {
  const query = useQuery<Utilisateur>({
    key: CURRENT_USER_QUERY_KEY,
    query: getMe,
    staleTime: Infinity,
  })

  const user = computed(() => query.data.value ?? null)
  const displayName = computed(() =>
    user.value ? `${user.value.prenom} ${user.value.nom}` : '',
  )

  return {
    user,
    displayName,
    status: query.status,
    isPending: query.isPending,
    error: query.error,
    refetch: query.refetch,
  }
}
