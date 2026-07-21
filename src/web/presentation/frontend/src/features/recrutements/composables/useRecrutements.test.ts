import type { RecrutementKey } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '../mock'
import { useRecrutements } from './useRecrutements'

vi.mock('../api', () => ({
  getRecrutementsActifs: vi.fn(),
  getRecrutementsArchives: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

function buildPaginatedResponse<T>(results: T[]) {
  return { count: results.length, next: null, previous: null, results }
}

function mountUseRecrutements(activeKey: ReturnType<typeof ref<RecrutementKey>>) {
  let result!: ReturnType<typeof useRecrutements>

  mount(defineComponent({
    setup() {
      result = useRecrutements(ORGANISME_UUID, () => activeKey.value as RecrutementKey)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })

  return result
}

describe('useRecrutements', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementsActifs).mockReset()
    vi.mocked(getRecrutementsArchives).mockReset()
    vi.mocked(getRecrutementsActifs).mockResolvedValue(buildPaginatedResponse(RECRUTEMENTS_ACTIFS))
    vi.mocked(getRecrutementsArchives).mockResolvedValue(buildPaginatedResponse(RECRUTEMENTS_ARCHIVES))
  })

  it('loads actifs when the actifs tab is active', async () => {
    const { data, pending } = mountUseRecrutements(ref<RecrutementKey>('actifs'))

    await vi.waitFor(() => expect(pending.value).toBe(false))

    expect(getRecrutementsActifs).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(data.actifs).toEqual(RECRUTEMENTS_ACTIFS)
  })

  it('does not load archives until the tab becomes active', async () => {
    const activeKey = ref<RecrutementKey>('actifs')
    const { data, pending } = mountUseRecrutements(activeKey)

    await vi.waitFor(() => expect(pending.value).toBe(false))
    expect(getRecrutementsArchives).not.toHaveBeenCalled()

    activeKey.value = 'archives'

    await vi.waitFor(() => expect(data.archives).toEqual(RECRUTEMENTS_ARCHIVES))
    expect(getRecrutementsArchives).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('exposes the error of the active tab on api failure', async () => {
    vi.mocked(getRecrutementsActifs).mockRejectedValue(new Error('emulated API error'))

    const { error, data, pending } = mountUseRecrutements(ref<RecrutementKey>('actifs'))

    await vi.waitFor(() => expect(pending.value).toBe(false))

    expect(error.value).toBeInstanceOf(Error)
    expect(data.actifs).toEqual([])
  })
})
