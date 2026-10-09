import { PiniaColada, useQueryCache } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID } from '@/test/fixtures/candidatures'
import { getRecrutementDetail } from '../api'
import { RECRUTEMENTS_QUERY_KEYS } from '../queries'
import { useRecrutementDetail } from './useRecrutementDetail'

vi.mock('../api', () => ({
  getRecrutementDetail: vi.fn(),
}))

const PARAMS = { organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }

function mountRecrutementDetail(seedCache?: () => void) {
  let context!: ReturnType<typeof useRecrutementDetail>
  mount(defineComponent({
    setup() {
      seedCache?.()
      context = useRecrutementDetail(PARAMS)
      return () => h('div')
    },
  }), { global: { plugins: [createPinia(), PiniaColada] } })
  return context
}

describe('useRecrutementDetail', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementDetail).mockReset().mockResolvedValue(RECRUTEMENT_DETAIL)
  })

  it('seeds the intitule from the recrutements list cache while pending', async () => {
    vi.mocked(getRecrutementDetail).mockImplementation(() => new Promise(() => {}))

    const context = mountRecrutementDetail(() => {
      useQueryCache().setQueryData(RECRUTEMENTS_QUERY_KEYS.actifs(ORGANISME_UUID), {
        count: 1,
        next: null,
        previous: null,
        results: [{ uuid: RECRUTEMENT_UUID, intitule: 'Chargé de mission numérique' }],
      })
    })

    expect(context.intitule.value).toBe('Chargé de mission numérique')
    expect(context.pending.value).toBe(true)
  })

  it('has no intitule while pending without cached list', () => {
    vi.mocked(getRecrutementDetail).mockImplementation(() => new Promise(() => {}))

    const context = mountRecrutementDetail()

    expect(context.intitule.value).toBeNull()
  })
})
