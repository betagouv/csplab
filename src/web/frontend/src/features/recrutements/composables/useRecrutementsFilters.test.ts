import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import { useRecrutementsFilters } from './useRecrutementsFilters'

describe('useRecrutementsFilters', () => {
  it('exposes the unfiltered list when no filter is applied', () => {
    const { filtered, activeFiltersCount } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    expect(filtered.value).toEqual(RECRUTEMENTS_ACTIFS)
    expect(activeFiltersCount.value).toBe(0)
  })

  it('only filters once draft is applied', () => {
    const { draft, apply, filtered, activeFiltersCount } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    draft.typeContrat = 'CONTRACTUELS'
    expect(filtered.value).toEqual(RECRUTEMENTS_ACTIFS)

    apply()
    expect(filtered.value.every(row => row.type_contrat === 'CONTRACTUELS')).toBe(true)
    expect(filtered.value.length).toBeGreaterThan(0)
    expect(filtered.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)
    expect(activeFiltersCount.value).toBe(1)
  })

  it('filters by responsable', () => {
    const { draft, apply, filtered } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    draft.responsable = 'Hugo Bernard'
    apply()
    expect(filtered.value.map(row => row.offer_id)).toEqual(['rec-3'])
  })

  it('restores full list on reset', () => {
    const { draft, apply, reset, filtered, canReset } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    draft.typeContrat = 'CONTRACTUELS'
    apply()
    expect(filtered.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)

    reset()
    expect(filtered.value).toEqual(RECRUTEMENTS_ACTIFS)
    expect(canReset.value).toBe(false)
  })
})

describe('useRecrutementsFilters: search', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('combines search with applied filters', async () => {
    const { draft, apply, search, filtered } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    draft.typeContrat = 'CONTRACTUELS'
    apply()
    search.value = 'zzz-no-match'
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(filtered.value).toEqual([])
  })

  it('clears search on reset', async () => {
    const { search, reset, filtered } = useRecrutementsFilters(RECRUTEMENTS_ACTIFS)
    search.value = 'back'
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(filtered.value.length).toBeLessThan(RECRUTEMENTS_ACTIFS.length)

    reset()
    await nextTick()
    vi.advanceTimersByTime(250)
    expect(search.value).toBe('')
    expect(filtered.value).toEqual(RECRUTEMENTS_ACTIFS)
  })
})
