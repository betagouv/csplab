import type { RecrutementBase } from '../types'
import { describe, expect, it } from 'vitest'
import {
  emptyRecrutementsFilters,
  matchesFilters,
  recrutementSearchableText,
} from './filters'

function makeRow(overrides: Partial<RecrutementBase> = {}): RecrutementBase {
  return {
    offer_id: 'rec-1',
    intitule: 'Chargé·e de mission',
    reference_csp: 'REF-001',
    responsables: [{ nom: 'Camille Durand' }],
    type_contrat: 'TITULAIRE_CONTRACTUEL',
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

  it('filters by responsable and type of contrat', () => {
    const responsableFilters = { ...emptyRecrutementsFilters(), responsable: 'Camille Durand' }
    expect(matchesFilters(makeRow(), responsableFilters)).toBe(true)
    expect(matchesFilters(makeRow({ responsables: [{ nom: 'John Doe' }] }), responsableFilters)).toBe(false)

    const typeFilters = { ...emptyRecrutementsFilters(), typeContrat: 'CONTRACTUELS' as const }
    expect(matchesFilters(makeRow(), typeFilters)).toBe(false)
    expect(matchesFilters(makeRow({ type_contrat: 'CONTRACTUELS' }), typeFilters)).toBe(true)
  })

  it('combines filters with a logical AND', () => {
    const filters = {
      responsable: 'Camille Durand',
      typeContrat: 'CONTRACTUELS' as const,
    }
    expect(matchesFilters(makeRow(), filters)).toBe(false)
    expect(matchesFilters(makeRow({ type_contrat: 'CONTRACTUELS' }), filters)).toBe(true)
  })
})

describe('recrutementSearchableText', () => {
  it('exposes intitulé, référence and responsable names', () => {
    const fields = recrutementSearchableText(makeRow({
      intitule: 'Développeur back-end',
      reference_csp: 'REF-042',
      responsables: [{ nom: 'Léa Martin' }],
    }))
    expect(fields).toContain('Développeur back-end')
    expect(fields).toContain('REF-042')
    expect(fields).toContain('Léa Martin')
  })

  it('includes the recruited person on archived offers', () => {
    const archived = makeRow({ intitule: 'Poste' }) as RecrutementBase & { recrute: string | null }
    archived.recrute = 'Nadia Lefèvre'
    expect(recrutementSearchableText(archived)).toContain('Nadia Lefèvre')
  })
})
