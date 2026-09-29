import { describe, expect, it } from 'vitest'
import { candidaturesViewOf, candidaturesViewQuery } from './useCandidaturesView'

describe('candidaturesViewOf', () => {
  it('reads the liste view from the query', () => {
    expect(candidaturesViewOf({ vue: 'liste' })).toBe('liste')
  })

  it('falls back to the kanban for an absent or unknown value', () => {
    expect(candidaturesViewOf({})).toBe('kanban')
    expect(candidaturesViewOf({ vue: 'kanban' })).toBe('kanban')
    expect(candidaturesViewOf({ vue: 'nimporte-quoi' })).toBe('kanban')
  })
})

describe('candidaturesViewQuery', () => {
  it('never writes the default view, so a state has a single url', () => {
    expect(candidaturesViewQuery('kanban')).toEqual({})
  })

  it('writes the liste view', () => {
    expect(candidaturesViewQuery('liste')).toEqual({ vue: 'liste' })
  })
})
