import type {
  EtapeRecrutementDetailedCandidatures,
  PaginatedCandidatureListeList,
} from '../types'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick, ref, shallowRef } from 'vue'
import { useCandidaturesFilters } from './useCandidaturesFilters'

const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
const ETAPE_PRESELECTION = 'cccccccc-0001-0001-0001-000000000002'

function makeEtapes(): EtapeRecrutementDetailedCandidatures[] {
  return [
    {
      etape_uuid: ETAPE_RECEPTION,
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
      etape_uuid: ETAPE_PRESELECTION,
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
        etape: { etape_uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
      },
      {
        uuid: 'dddddddd-0001-0001-0001-000000000002',
        date_soumission: '2025-06-11T14:30:00Z',
        date_derniere_activite: '2025-06-12T09:15:00Z',
        candidat: { uuid: 'eeeeeeee-0002', nom: 'Martin', prenom: 'Bruno' },
        etape: { etape_uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
      },
      {
        uuid: 'dddddddd-0001-0001-0001-000000000005',
        date_soumission: '2025-06-08T10:00:00Z',
        date_derniere_activite: '2025-06-11T10:00:00Z',
        candidat: { uuid: 'eeeeeeee-0005', nom: 'Bernard', prenom: 'Élise' },
        etape: { etape_uuid: ETAPE_PRESELECTION, nom: 'Présélection', categorie: 'EN_COURS' },
      },
    ],
  }
}

function setup() {
  const etapes = shallowRef(makeEtapes())
  const liste = ref<PaginatedCandidatureListeList | undefined>(makeListe())
  return { etapes, liste, filters: useCandidaturesFilters(etapes, liste) }
}

describe('useCandidaturesFilters', () => {
  it('exposes unfiltered data when no filter is active', () => {
    const { filters } = setup()
    expect(filters.filteredEtapes.value).toHaveLength(2)
    expect(filters.filteredCandidatures.value).toHaveLength(3)
    expect(filters.activeFiltersCount.value).toBe(0)
  })

  it('builds etape options from the etapes list', () => {
    const { filters } = setup()
    expect(filters.etapeOptions.value).toEqual([
      { value: ETAPE_RECEPTION, label: 'Réception des candidatures' },
      { value: ETAPE_PRESELECTION, label: 'Présélection' },
    ])
  })

  it('filters kanban columns and liste rows by etape once applied', () => {
    const { filters } = setup()
    filters.draft.etapes = [ETAPE_PRESELECTION]
    expect(filters.filteredEtapes.value).toHaveLength(2)

    filters.apply()
    expect(filters.filteredEtapes.value.map(e => e.nom)).toEqual(['Présélection'])
    expect(filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Bernard'])
    expect(filters.activeFiltersCount.value).toBe(1)
  })

  it('flushes search immediately without waiting for the debounce', () => {
    const { filters } = setup()
    filters.search.value = 'martin'
    filters.flushSearch()

    expect(filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Martin'])
  })

  it('falls back to an empty list when candidatureListe is undefined', () => {
    const etapes = shallowRef(makeEtapes())
    const liste = ref<PaginatedCandidatureListeList | undefined>(undefined)
    const filters = useCandidaturesFilters(etapes, liste)

    expect(filters.filteredCandidatures.value).toEqual([])
  })

  it('clears etape filter and search on reset', () => {
    const { filters } = setup()
    filters.draft.etapes = [ETAPE_PRESELECTION]
    filters.apply()
    filters.search.value = 'alice'
    filters.flushSearch()

    filters.reset()

    expect(filters.filteredEtapes.value).toHaveLength(2)
    expect(filters.filteredCandidatures.value).toHaveLength(3)
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
    expect(filters.filteredCandidatures.value).toHaveLength(3)

    vi.advanceTimersByTime(500)
    await nextTick()

    expect(filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Dupont'])
    expect(filters.filteredEtapes.value[0]?.candidatures.map(c => c.candidat.nom)).toEqual(['Dupont'])
  })
})
