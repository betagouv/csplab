import type { CreateCompteUtilisateurPayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { createCompteUtilisateur, resendInvitation } from '../api'
import { comptesUtilisateursQuery, ORGANISMES_QUERY_KEYS } from '../queries'

export function useComptesUtilisateurs(organismeUuid: string) {
  const queryCache = useQueryCache()
  const query = useQuery(comptesUtilisateursQuery({ organismeUuid }))

  function invalidate() {
    return queryCache.invalidateQueries({
      key: [...ORGANISMES_QUERY_KEYS.root, organismeUuid, 'comptes'],
    })
  }

  const createMutation = useMutation({
    mutation: (payload: CreateCompteUtilisateurPayload) =>
      createCompteUtilisateur(organismeUuid, payload),
    onSettled: invalidate,
  })

  const resendMutation = useMutation({
    mutation: (compteUuid: string) => resendInvitation(organismeUuid, compteUuid),
  })

  return {
    comptes: query.data,
    pending: query.isPending,
    error: query.error,
    create: createMutation.mutateAsync,
    creating: createMutation.isLoading,
    resend: resendMutation.mutateAsync,
    resending: resendMutation.isLoading,
  }
}
