import type {
  EtapeRecrutement,
  EtapeRecrutementDetailedCandidatures,
  PaginatedCandidatureListeList,
} from '../types'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick, shallowRef } from 'vue'
import { createCandidaturesFilters } from './useCandidaturesFilters'

const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
const ETAPE_PRESELECTION = 'cccccccc-0001-0001-0001-000000000002'
const ETAPE_ENTRETIEN = 'cccccccc-0001-0001-0001-000000000003'

function makeRecrutementEtapes(): EtapeRecrutement[] {
  return [
    { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
    { uuid: ETAPE_PRESELECTION, nom: 'Présélection', categorie: 'EN_COURS' },
    { uuid: ETAPE_ENTRETIEN, nom: 'Entretien', categorie: 'EN_COURS' },
  ]
}

function makeEtapes(): EtapeRecrutementDetailedCandidatures[] {
  return [
    {
      uuid: ETAPE_RECEPTION,
      nom: 'Réception des candidatures',
      categorie: 'ENTREE',
      candidatures: [
        {
          uuid: 'dddddddd-0001-0001-0001-000000000001',
          date_soumission: '2025-06-10T09:15:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001', nom: 'Dupont', prenom: 'Alice' },
        },
        {
          uuid: 'dddddddd-0001-0001-0001-000000000002',
          date_soumission: '2025-06-11T14:30:00Z',
          date_derniere_activite: '2025-06-12T09:15:00Z',
          candidat: { uuid: 'eeeeeeee-0002', nom: 'Martin', prenom: 'Bruno' },
        },
      ],
    },
    {
      uuid: ETAPE_PRESELECTION,
      nom: 'Présélection',
      categorie: 'EN_COURS',
      candidatures: [
        {
          uuid: 'dddddddd-0001-0001-0001-000000000005',
          date_soumission: '2025-06-08T10:00:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0005', nom: 'Bernard', prenom: 'Élise' },
        },
      ],
    },
  ]
}

function makeListe(): PaginatedCandidatureListeList {
  return {
    count: 3,
    next: null,
    previous: null,
    results: [
      {
        uuid: 'dddddddd-0001-0001-0001-000000000001',
        date_soumission: '2025-06-10T09:15:00Z',
        date_derniere_activite: '2025-06-11T10:00:00Z',
        candidat: { uuid: 'eeeeeeee-0001', nom: 'Dupont', prenom: 'Alice' },
        etape: { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
      },
      {
        uuid: 'dddddddd-0001-0001-0001-000000000002',
        date_soumission: '2025-06-11T14:30:00Z',
        date_derniere_activite: '2025-06-12T09:15:00Z',
        candidat: { uuid: 'eeeeeeee-0002', nom: 'Martin', prenom: 'Bruno' },
        etape: { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
      },
      {
        uuid: 'dddddddd-0001-0001-0001-000000000005',
        date_soumission: '2025-06-08T10:00:00Z',
        date_derniere_activite: '2025-06-11T10:00:00Z',
        candidat: { uuid: 'eeeeeeee-0005', nom: 'Bernard', prenom: 'Élise' },
        etape: { uuid: ETAPE_PRESELECTION, nom: 'Présélection', categorie: 'EN_COURS' },
      },
    ],
  }
}

function setup() {
  return { filters: createCandidaturesFilters(shallowRef(makeRecrutementEtapes())) }
}

describe('useCandidaturesFilters', () => {
  it('exposes unfiltered data when no filter is active', () => {
    const { filters } = setup()
    expect(filters.filterEtapes(makeEtapes())).toHaveLength(2)
    expect(filters.filterCandidatures(makeListe().results)).toHaveLength(3)
    expect(filters.activeFiltersCount.value).toBe(0)
  })

  it('builds etape options from the recrutement etapes', () => {
    const { filters } = setup()
    expect(filters.etapeOptions.value).toEqual([
      { value: ETAPE_RECEPTION, label: 'Réception des candidatures' },
      { value: ETAPE_PRESELECTION, label: 'Présélection' },
      { value: ETAPE_ENTRETIEN, label: 'Entretien' },
    ])
  })

  it('filters kanban columns and liste rows by etape once applied', () => {
    const { filters } = setup()
    filters.draft.etapes = [ETAPE_PRESELECTION]
    expect(filters.filterEtapes(makeEtapes())).toHaveLength(2)

    filters.apply()
    expect(filters.filterEtapes(makeEtapes()).map(e => e.nom)).toEqual(['Présélection'])
    expect(filters.filterCandidatures(makeListe().results).map(c => c.candidat.nom)).toEqual(['Bernard'])
    expect(filters.activeFiltersCount.value).toBe(1)
  })

  it('flushes search immediately without waiting for the debounce', () => {
    const { filters } = setup()
    filters.search.value = 'martin'
    filters.flushSearch()

    expect(filters.filterCandidatures(makeListe().results).map(c => c.candidat.nom)).toEqual(['Martin'])
  })

  it('clears etape filter and search on reset', () => {
    const { filters } = setup()
    filters.draft.etapes = [ETAPE_PRESELECTION]
    filters.apply()
    filters.search.value = 'alice'
    filters.flushSearch()

    filters.reset()

    expect(filters.filterEtapes(makeEtapes())).toHaveLength(2)
    expect(filters.filterCandidatures(makeListe().results)).toHaveLength(3)
    expect(filters.search.value).toBe('')
    expect(filters.canReset.value).toBe(false)
  })
})

describe('useCandidaturesFilters: debounced search', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('applies the search term after the debounce delay', async () => {
    const { filters } = setup()
    filters.search.value = 'alice'
    await nextTick()
    expect(filters.filterCandidatures(makeListe().results)).toHaveLength(3)

    vi.advanceTimersByTime(500)
    await nextTick()

    expect(filters.filterCandidatures(makeListe().results).map(c => c.candidat.nom)).toEqual(['Dupont'])
    expect(filters.filterEtapes(makeEtapes())[0]?.candidatures.map(c => c.candidat.nom)).toEqual(['Dupont'])
  })
})
