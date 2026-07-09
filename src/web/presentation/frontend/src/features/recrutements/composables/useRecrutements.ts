import type {
  RecrutementKey,
  RecrutementsActifs,
  RecrutementsArchives,
} from '../types'
import { reactive } from 'vue'
import { useAsyncState } from '@/composables/async/useAsyncState'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api'

export function useRecrutements(organismeUuid: string) {
  const { pending, error, run } = useAsyncState(true)

  const data = reactive({
    actifs: [] as RecrutementsActifs[],
    archives: [] as RecrutementsArchives[],
  })

  function has(key: RecrutementKey): boolean {
    return data[key].length > 0
  }

  async function load(key: RecrutementKey = 'actifs'): Promise<void> {
    await run(async () => {
      if (key === 'actifs') {
        const actifs = await getRecrutementsActifs(organismeUuid)
        data.actifs = actifs.results as RecrutementsActifs[]
      }
      else {
        const archives = await getRecrutementsArchives(organismeUuid)
        data.archives = archives.results as RecrutementsArchives[]
      }
    })
  }

  return {
    pending,
    error,
    data,
    load,
    has,
  }
}
