import type { Candidat } from '../types'
import { describe, expect, it } from 'vitest'
import {
  countActiveFilters,
  emptyCandidaturesFilters,
  matchesEtape,
  matchesSearch,
} from './filters'

function makeCandidat(overrides: Partial<Candidat> = {}): Candidat {
  return {
    uuid: 'candidat-1',
    nom: 'Lefèvre',
    prenom: 'Élise',
    ...overrides,
  }
}

describe('matchesEtape', () => {
  it('matches every etape when no filter is set', () => {
    expect(matchesEtape('etape-1', emptyCandidaturesFilters())).toBe(true)
  })

  it('matches only selected etapes', () => {
    const filters = { etapes: ['etape-1', 'etape-2'] }
    expect(matchesEtape('etape-1', filters)).toBe(true)
    expect(matchesEtape('etape-3', filters)).toBe(false)
  })
})

describe('countActiveFilters', () => {
  it('counts the etapes selection as a single filter', () => {
    expect(countActiveFilters(emptyCandidaturesFilters())).toBe(0)
    expect(countActiveFilters({ etapes: ['etape-1', 'etape-2'] })).toBe(1)
  })
})

describe('matchesSearch', () => {
  it('matches every candidat on a blank search', () => {
    expect(matchesSearch(makeCandidat(), '')).toBe(true)
    expect(matchesSearch(makeCandidat(), '   ')).toBe(true)
  })

  it('matches on nom and prenom regardless of order', () => {
    expect(matchesSearch(makeCandidat(), 'lefevre')).toBe(true)
    expect(matchesSearch(makeCandidat(), 'elise')).toBe(true)
    expect(matchesSearch(makeCandidat(), 'elise lef')).toBe(true)
    expect(matchesSearch(makeCandidat(), 'lefevre el')).toBe(true)
  })

  it('is case- and accent-insensitive', () => {
    expect(matchesSearch(makeCandidat(), 'LEFÈVRE')).toBe(true)
  })

  it('returns false when the name does not contain the term', () => {
    expect(matchesSearch(makeCandidat(), 'dupont')).toBe(false)
  })
})
