import { useQuery } from '@pinia/colada'
import { organismesListQuery } from '../queries'

export function useOrganismes() {
  const query = useQuery(organismesListQuery)

  return {
    organismesList: query.data,
    pending: query.isPending,
    error: query.error,
  }
}
