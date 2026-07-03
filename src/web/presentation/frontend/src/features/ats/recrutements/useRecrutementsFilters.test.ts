import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick, reactive } from 'vue'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from './mock'
import { useRecrutementsFilters } from './useRecrutementsFilters'

function makeData() {
  return reactive({
    actifs: RECRUTEMENTS_ACTIFS,
    archives: RECRUTEMENTS_ARCHIVES,
  })
}

describe('useRecrutementsFilters', () => {
  it('exposes unfiltered lists when no filter is applied', () => {
    const { filteredActifs, filteredArchives, activeFiltersCount } = useRecrutementsFilters(makeData())
    expect(filteredActifs.value).toEqual(RECRUTEMENTS_ACTIFS)
    expect(filteredArchives.value).toEqual(RECRUTEMENTS_ARCHIVES)
    expect(activeFiltersCount.value).toBe(0)
  })

  it('only filters once draft is applied', () => {
    const { draft, apply, filteredActifs, activeFiltersCount } = useRecrutementsFilters(makeData())
    draft.typeContrat = 'CONTRACTUELS'
    expect(filteredActifs.value).toEqual(RECRUTEMENTS_ACTIFS)

    apply()
    expect(filteredActifs.value.every(row => row.type_contrat === 'CONTRACTUELS')).toBe(true)
    expect(filteredActifs.value.length).toBeGreaterThan(0)
    expect(filteredActifs.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)
    expect(activeFiltersCount.value).toBe(1)
  })

  it('filters both tabs from the same applied state', () => {
    const { draft, apply, filteredActifs, filteredArchives } = useRecrutementsFilters(makeData())
    draft.responsable = 'Hugo Bernard'
    apply()
    expect(filteredActifs.value.map(row => row.offer_id)).toEqual(['rec-3'])
    expect(filteredArchives.value.map(row => row.offer_id)).toEqual(['arch-1'])
  })

  it('restores full lists on reset', () => {
    const { draft, apply, reset, filteredActifs, canReset } = useRecrutementsFilters(makeData())
    draft.kindContrat = 'CDD'
    apply()
    expect(filteredActifs.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)

    reset()
    expect(filteredActifs.value).toEqual(RECRUTEMENTS_ACTIFS)
    expect(canReset.value).toBe(false)
  })
})

describe('useRecrutementsFilters: search', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('combines search with applied filters', async () => {
    const { draft, apply, search, filteredActifs } = useRecrutementsFilters(makeData())
    draft.typeContrat = 'CONTRACTUELS'
    apply()
    search.value = 'zzz-no-match'
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(filteredActifs.value).toEqual([])
  })

  it('clears search on reset', async () => {
    const { search, reset, filteredActifs } = useRecrutementsFilters(makeData())
    search.value = 'back'
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(filteredActifs.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)

    reset()
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(search.value).toBe('')
    expect(filteredActifs.value).toEqual(RECRUTEMENTS_ACTIFS)
  })
})
