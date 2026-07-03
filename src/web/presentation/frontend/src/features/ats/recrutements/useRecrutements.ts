import type {
  RecrutementActif,
  RecrutementArchive,
} from './types'
import { reactive, ref } from 'vue'
import { getRecrutements } from '../api/recrutement'

const FETCH_SIZE = 100

export function useRecrutements(organismeUuid: string) {
  const state = ref<'idle' | 'loading' | 'error' | 'success'>('idle')

  const data = reactive({
    actifs: [] as RecrutementActif[],
    archives: [] as RecrutementArchive[],
  })

  const error = ref<Error | null>(null)

  async function load(): Promise<void> {
    state.value = 'loading'
    try {
      const [actifs, archives] = await Promise.all([
        getRecrutements(organismeUuid, { filtre: 'actifs', size: FETCH_SIZE }),
        getRecrutements(organismeUuid, { filtre: 'archives', size: FETCH_SIZE }),
      ])
      data.actifs = actifs.results as RecrutementActif[]
      data.archives = archives.results as RecrutementArchive[]
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
  }
}
