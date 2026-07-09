import type {
  RecrutementKey,
  RecrutementsActifs,
  RecrutementsArchives,
} from '../types'
import { reactive, ref } from 'vue'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '../mock'

export function useRecrutements(options: {
  organismeUuid?: string
  source?: 'api' | 'mock'
} = {}) {
  const state = ref<'idle' | 'loading' | 'error' | 'success'>('idle')
  const source = options.source ?? 'api'

  const data = reactive({
    actifs: [] as RecrutementsActifs[],
    archives: [] as RecrutementsArchives[],
  })

  const error = ref<Error | null>(null)

  function has(key: RecrutementKey): boolean {
    return data[key].length > 0
  }

  async function load(
    key: RecrutementKey = 'actifs',
  ): Promise<void> {
    state.value = 'loading'
    try {
      if (source === 'mock') {
        if (key === 'actifs') {
          data.actifs = RECRUTEMENTS_ACTIFS
        }
        else {
          data.archives = RECRUTEMENTS_ARCHIVES
        }
        return
      }

      if (!options.organismeUuid) {
        throw new Error('organismeUuid is required when source is api')
      }

      if (key === 'actifs') {
        const actifs = await getRecrutementsActifs(options.organismeUuid)
        data.actifs = actifs.results as RecrutementsActifs[]
      }
      else {
        const archives = await getRecrutementsArchives(options.organismeUuid)
        data.archives = archives.results as RecrutementsArchives[]
      }
    }
    catch (err) {
      state.value = 'error'
      error.value = err instanceof Error ? err : new Error('Unknown error')
    }
    finally {
      if (state.value !== 'error') {
        state.value = 'success'
      }
    }
  }

  return {
    state,
    error,
    data,
    load,
    has,
  }
}
