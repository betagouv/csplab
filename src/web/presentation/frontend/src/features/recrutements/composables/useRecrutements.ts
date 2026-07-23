import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementKey } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, reactive, toValue } from 'vue'
import { recrutementsActifsQuery, recrutementsArchivesQuery } from '../queries'

export function useRecrutements(
  organismeUuid: string,
  activeKey: MaybeRefOrGetter<RecrutementKey>,
) {
  const actifs = useQuery(() => ({
    ...recrutementsActifsQuery({ organismeUuid }),
    enabled: toValue(activeKey) === 'actifs',
  }))

  const archives = useQuery(() => ({
    ...recrutementsArchivesQuery({ organismeUuid }),
    enabled: toValue(activeKey) === 'archives',
  }))

  const active = computed(() => (toValue(activeKey) === 'actifs' ? actifs : archives))

  const data = reactive({
    actifs: computed(() => actifs.data.value?.results ?? []),
    archives: computed(() => archives.data.value?.results ?? []),
  })

  const pending = computed(() => active.value.isPending.value)
  const error = computed(() => active.value.error.value)

  const pendingActifs = computed(
    () => toValue(activeKey) === 'actifs' && actifs.isPending.value,
  )
  const pendingArchives = computed(
    () => toValue(activeKey) === 'archives' && archives.isPending.value,
  )

  return {
    pending,
    pendingActifs,
    pendingArchives,
    error,
    data,
  }
}
