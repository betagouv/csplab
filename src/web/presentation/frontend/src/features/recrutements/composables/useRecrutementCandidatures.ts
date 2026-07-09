import type { PaginatedCandidatureListeResponse, RecrutementDetail } from '../types'
import { ref } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getCandidatureListe, getRecrutementDetail } from '../api'

export function useRecrutementCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
) {
  const { pending, error, run } = useAsyncState(true)
  const candidatureListe = ref<PaginatedCandidatureListeResponse>()
  const recrutementDetail = ref<RecrutementDetail>()

  async function load(): Promise<void> {
    await run(async () => {
      const [detail, liste] = await Promise.all([
        getRecrutementDetail({ organismeUuid, recrutementUuid }),
        getCandidatureListe({ organismeUuid, recrutementUuid }),
      ])

      recrutementDetail.value = detail
      candidatureListe.value = liste
    })
  }

  return {
    pending,
    error,
    candidatureListe,
    recrutementDetail,
    load,
  }
}
