import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { equipeRecrutementQuery } from '../queries'

export function useEquipeRecrutement(organismeUuid: string, recrutementUuid: string) {
  const query = useQuery(() => equipeRecrutementQuery({ organismeUuid, recrutementUuid }))

  return {
    membres: computed(() => query.data.value ?? []),
    pending: query.isPending,
    error: query.error,
  }
}
