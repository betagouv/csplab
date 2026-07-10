import type { PaginatedCandidatureListeResponse, RecrutementDetailKanban } from '../types'
import { ref } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getCandidatureListe, getRecrutementKanban } from '../api'

export function useCandidaturesListe(
  organismeUuid: string,
  recrutementUuid: string,
) {
  const { pending, error, run } = useAsyncState(true)
  const candidatureListe = ref<PaginatedCandidatureListeResponse>()
  const recrutementDetail = ref<RecrutementDetailKanban>()

  async function load(): Promise<void> {
    await run(async () => {
      const [detail, liste] = await Promise.all([
        getRecrutementKanban(organismeUuid, recrutementUuid),
        getCandidatureListe(organismeUuid, recrutementUuid),
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
