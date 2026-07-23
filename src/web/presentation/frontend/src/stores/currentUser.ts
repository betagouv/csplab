import type { Utilisateur } from '@/api/utilisateur'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { getMe } from '@/api/utilisateur'

export function useCurrentUser() {
  const query = useQuery<Utilisateur>({
    key: ['currentUser'],
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
