import { useQuery } from '@pinia/colada'
import { organismesQuery } from '../queries'

export function useOrganismes() {
  const query = useQuery(organismesQuery)

  return {
    organismes: query.data,
    pending: query.isPending,
    error: query.error,
  }
}
