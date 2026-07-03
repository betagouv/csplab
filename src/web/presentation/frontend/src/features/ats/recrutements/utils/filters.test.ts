import type { RecrutementBase } from '../types'
import { describe, expect, it } from 'vitest'
import {
  emptyRecrutementsFilters,
  matchesFilters,
  matchesSearch,
} from './filters'

function makeRow(overrides: Partial<RecrutementBase> = {}): RecrutementBase {
  return {
    offer_id: 'rec-1',
    intitule: 'Chargé·e de mission',
    reference_csp: 'REF-001',
    responsables: [{ nom: 'Camille Durand' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
    kind_contrat: null,
    date_publication: '2026-07-01T12:00:00Z',
    derniere_activite: '2026-07-02T12:00:00Z',
    candidatures: null,
    ...overrides,
  }
}

describe('matchesFilters', () => {
  it('matches everything when no filter is set', () => {
    expect(matchesFilters(makeRow(), emptyRecrutementsFilters())).toBe(true)
  })

  it('filters by responsable, type and kind of contrat', () => {
    const responsableFilters = { ...emptyRecrutementsFilters(), responsable: 'Camille Durand' }
    expect(matchesFilters(makeRow(), responsableFilters)).toBe(true)
    expect(matchesFilters(makeRow({ responsables: [{ nom: 'John Doe' }] }), responsableFilters)).toBe(false)

    const typeFilters = { ...emptyRecrutementsFilters(), typeContrat: 'CONTRACTUELS' as const }
    expect(matchesFilters(makeRow(), typeFilters)).toBe(false)
    expect(matchesFilters(makeRow({ type_contrat: 'CONTRACTUELS' }), typeFilters)).toBe(true)

    const kindFilters = { ...emptyRecrutementsFilters(), kindContrat: 'CDD' as const }
    expect(matchesFilters(makeRow(), kindFilters)).toBe(false)
    expect(matchesFilters(makeRow({ kind_contrat: 'CDD' }), kindFilters)).toBe(true)
  })

  it('combines filters with a logical AND', () => {
    const filters = {
      responsable: 'Camille Durand',
      typeContrat: 'CONTRACTUELS' as const,
      kindContrat: null,
    }
    expect(matchesFilters(makeRow(), filters)).toBe(false)
    expect(matchesFilters(makeRow({ type_contrat: 'CONTRACTUELS' }), filters)).toBe(true)
  })
})

describe('matchesSearch', () => {
  it('matches every row on a blank search', () => {
    expect(matchesSearch(makeRow(), '')).toBe(true)
    expect(matchesSearch(makeRow(), '   ')).toBe(true)
  })

  it('matches on intitulé, référence and responsable name', () => {
    expect(matchesSearch(makeRow({ intitule: 'Développeur back-end' }), 'back')).toBe(true)
    expect(matchesSearch(makeRow({ reference_csp: 'REF-042' }), 'ref-042')).toBe(true)
    expect(matchesSearch(makeRow({ responsables: [{ nom: 'Léa Martin' }] }), 'martin')).toBe(true)
  })

  it('is case- and accent-insensitive', () => {
    expect(matchesSearch(makeRow({ intitule: 'Chargé de mission' }), 'CHARGE')).toBe(true)
  })

  it('returns false when no searchable field contains the term', () => {
    expect(matchesSearch(makeRow({ intitule: 'Juriste' }), 'zzz')).toBe(false)
  })

  it('matches recruited person on archived offers', () => {
    const archived = makeRow({ intitule: 'Poste' }) as RecrutementBase & { recrute: string | null }
    archived.recrute = 'Nadia Lefèvre'
    expect(matchesSearch(archived, 'nadia')).toBe(true)
  })
})
