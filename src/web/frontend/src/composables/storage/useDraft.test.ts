import { describe, expect, it } from 'vitest'
import { useDraft } from './useDraft'

interface Filters extends Record<string, unknown> {
  name: string | null
  kind: string | null
}

function makeEmpty(): Filters {
  return { name: null, kind: null }
}

describe('useDraft', () => {
  it('starts clean with draft and applied at initial values', () => {
    const { draft, applied, hasDiverged, canReset } = useDraft(makeEmpty)
    expect(draft).toEqual(makeEmpty())
    expect(applied).toEqual(makeEmpty())
    expect(hasDiverged.value).toBe(false)
    expect(canReset.value).toBe(false)
  })

  it('tracks when draft diverges from applied', () => {
    const { draft, hasDiverged } = useDraft(makeEmpty)
    draft.name = 'Camille'
    expect(hasDiverged.value).toBe(true)
  })

  it('applies draft to applied state', () => {
    const { draft, applied, hasDiverged, apply } = useDraft(makeEmpty)
    draft.name = 'Camille'
    apply()
    expect(applied.name).toBe('Camille')
    expect(hasDiverged.value).toBe(false)
  })

  it('syncs draft back from applied state', () => {
    const { draft, applied, syncDraft, apply } = useDraft(makeEmpty)
    draft.name = 'Camille'
    apply()
    draft.name = 'Léa'
    syncDraft()
    expect(draft.name).toBe('Camille')
    expect(applied.name).toBe('Camille')
  })

  it('resets both draft and applied to initial values', () => {
    const { draft, applied, canReset, apply, reset } = useDraft(makeEmpty)
    draft.name = 'Camille'
    apply()
    expect(canReset.value).toBe(true)
    reset()
    expect(draft).toEqual(makeEmpty())
    expect(applied).toEqual(makeEmpty())
    expect(canReset.value).toBe(false)
  })

  it('allows reset only when draft diverges from initial', () => {
    const { draft, canReset } = useDraft(makeEmpty)
    draft.kind = 'CDD'
    expect(canReset.value).toBe(true)
  })

  describe('array values', () => {
    interface ArrayFilters extends Record<string, unknown> {
      etapes: string[]
    }

    function makeEmptyArrays(): ArrayFilters {
      return { etapes: [] }
    }

    it('compares arrays by content', () => {
      const { draft, hasDiverged, canReset, apply } = useDraft(makeEmptyArrays)
      expect(hasDiverged.value).toBe(false)
      expect(canReset.value).toBe(false)

      draft.etapes = ['a']
      expect(hasDiverged.value).toBe(true)

      apply()
      expect(hasDiverged.value).toBe(false)
      expect(canReset.value).toBe(true)
    })

    it('stays clean after resetting array values', () => {
      const { draft, apply, reset, canReset } = useDraft(makeEmptyArrays)
      draft.etapes = ['a', 'b']
      apply()
      reset()
      expect(canReset.value).toBe(false)
    })

    it('copies arrays so draft and applied stay independent', () => {
      const { draft, applied, apply, hasDiverged } = useDraft(makeEmptyArrays)
      draft.etapes = ['a']
      apply()
      draft.etapes.push('b')
      expect(applied.etapes).toEqual(['a'])
      expect(hasDiverged.value).toBe(true)
    })
  })
})
