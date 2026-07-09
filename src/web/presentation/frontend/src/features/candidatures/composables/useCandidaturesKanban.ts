import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementDetailKanban } from '../types'
import { computed, ref, toValue } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getRecrutementKanban } from '../api'

export function useCandidaturesKanban(
  organismeUuid: MaybeRefOrGetter<string>,
  recrutementUuid: MaybeRefOrGetter<string>,
) {
  const { pending, error, run } = useAsyncState(true)
  const kanban = ref<RecrutementDetailKanban | null>(null)

  const etapes = computed(() => kanban.value?.etapes ?? [])

  const totalCount = computed(() =>
    etapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0),
  )

  async function load(): Promise<void> {
    await run(async () => {
      kanban.value = await getRecrutementKanban(
        toValue(organismeUuid),
        toValue(recrutementUuid),
      )
    })
  }

  return {
    kanban,
    etapes,
    totalCount,
    pending,
    error,
    load,
  }
}
