import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { searchOrganismes } from '../api'
import { useOrganismesSearch } from './useOrganismesSearch'

vi.mock('../api', () => ({
  searchOrganismes: vi.fn(),
}))

function pause(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const RESULTAT = { uuid: 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', nom: 'Commune de Briançon', siret: '21050023500017' }

function mountSearch() {
  let result!: ReturnType<typeof useOrganismesSearch>
  mount(defineComponent({
    setup() {
      result = useOrganismesSearch()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useOrganismesSearch', () => {
  beforeEach(() => {
    vi.mocked(searchOrganismes).mockReset().mockResolvedValue([RESULTAT])
  })

  it('waits for three characters before searching', async () => {
    const { search, results } = mountSearch()

    search.value = 'br '
    await pause(400)

    expect(searchOrganismes).not.toHaveBeenCalled()
    expect(results.value).toEqual([])
  })

  it('searches the trimmed term once typing pauses', async () => {
    const { search, results } = mountSearch()

    search.value = 'bri'
    await pause(100)
    search.value = 'brian'
    await pause(100)
    search.value = ' brianç '

    await vi.waitFor(() => expect(results.value).toEqual([RESULTAT]))
    expect(searchOrganismes).toHaveBeenCalledTimes(1)
    expect(searchOrganismes).toHaveBeenCalledWith('brianç')
  })
})
