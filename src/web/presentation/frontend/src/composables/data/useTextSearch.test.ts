import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { effectScope, nextTick } from 'vue'
import { useTextSearch } from './useTextSearch'

interface Row {
  nom: string
  siret: string | null
}

const ROWS: Row[] = [
  { nom: 'Ministère de l\'Intérieur', siret: '11000101300017' },
  { nom: 'Préfecture de Paris', siret: null },
  { nom: 'Mairie de Lyon', siret: '21690123400018' },
]

function withScope<T>(fn: () => T): T {
  const scope = effectScope()
  return scope.run(fn) as T
}

describe('useTextSearch', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  async function setSearch(search: { value: string }, term: string): Promise<void> {
    search.value = term
    await nextTick()
    vi.advanceTimersByTime(250)
  }

  it('returns all rows when the search is empty', () => {
    const { filtered } = withScope(() =>
      useTextSearch(ROWS, row => [row.nom, row.siret]),
    )
    expect(filtered.value).toHaveLength(3)
  })

  it('filters on the provided fields, ignoring accents and case', async () => {
    const { search, filtered } = withScope(() =>
      useTextSearch(ROWS, row => [row.nom, row.siret]),
    )

    await setSearch(search, 'ministere')

    expect(filtered.value).toEqual([ROWS[0]])
  })

  it('matches on any searchable field and skips null values', async () => {
    const { search, filtered } = withScope(() =>
      useTextSearch(ROWS, row => [row.nom, row.siret]),
    )

    await setSearch(search, '2169')

    expect(filtered.value).toEqual([ROWS[2]])
  })
})
