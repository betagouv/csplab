import type { PaginatedCandidatureListeList, RecrutementDetailKanban } from '../types'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { RECRUTEMENTS_QUERY_KEYS } from '@/features/recrutements/queries'
import { getCandidatureListe, getRecrutementKanban } from '../api'
import { CANDIDATURES_QUERY_KEYS } from '../queries'
import { useCandidatures } from './useCandidatures'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

const MOCK_KANBAN: RecrutementDetailKanban = {
  offer_id: RECRUTEMENT_UUID,
  intitule: 'Chargé de mission numérique',
  date_publication: '2025-06-22T10:00:00Z',
  localisation: {
    zone_geographique: 'EU',
    pays: 'FRA',
    region: '11',
    departement: '75',
    localisation_label: 'Paris 8e arrondissement',
    latitude: 48.8748,
    longitude: 2.3070,
  },
  organisme_recruteur: { nom: 'Mairie de Paris', siret: '21750001600019' },
  categorie_offre: 'A',
  etapes: [
    {
      etape_uuid: 'cccccccc-0001-0001-0001-000000000001',
      nom: 'Réception des candidatures',
      categorie: 'ENTREE',
      candidatures: [
        {
          uuid: 'dddddddd-0001-0001-0001-000000000001',
          date_soumission: '2025-06-10T09:15:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
        },
        {
          uuid: 'dddddddd-0001-0001-0001-000000000002',
          date_soumission: '2025-06-11T14:30:00Z',
          date_derniere_activite: '2025-06-12T09:15:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' },
        },
      ],
    },
    {
      etape_uuid: 'cccccccc-0001-0001-0001-000000000002',
      nom: 'Présélection',
      categorie: 'EN_COURS',
      candidatures: [
        {
          uuid: 'dddddddd-0001-0001-0001-000000000005',
          date_soumission: '2025-06-08T10:00:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000005', nom: 'Bernard', prenom: 'Élise' },
        },
      ],
    },
  ],
}

const MOCK_LISTE: PaginatedCandidatureListeList = {
  count: 3,
  next: null,
  previous: null,
  results: [
    {
      uuid: 'dddddddd-0001-0001-0001-000000000001',
      date_soumission: '2025-06-10T09:15:00Z',
      date_derniere_activite: '2025-06-11T10:00:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
      etape: { etape_uuid: 'cccccccc-0001-0001-0001-000000000001', nom: 'Réception des candidatures', categorie: 'ENTREE' },
    },
    {
      uuid: 'dddddddd-0001-0001-0001-000000000002',
      date_soumission: '2025-06-11T14:30:00Z',
      date_derniere_activite: '2025-06-12T09:15:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' },
      etape: { etape_uuid: 'cccccccc-0001-0001-0001-000000000001', nom: 'Réception des candidatures', categorie: 'ENTREE' },
    },
    {
      uuid: 'dddddddd-0001-0001-0001-000000000005',
      date_soumission: '2025-06-08T10:00:00Z',
      date_derniere_activite: '2025-06-11T10:00:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000005', nom: 'Bernard', prenom: 'Élise' },
      etape: { etape_uuid: 'cccccccc-0001-0001-0001-000000000002', nom: 'Présélection', categorie: 'EN_COURS' },
    },
  ],
}

const StubView = defineComponent({ render: () => h('div') })

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: StubView },
      { path: '/mes-recrutements/:recrutementUuid', component: StubView },
    ],
  })
}

async function mountCandidatures(onSetup?: () => void) {
  const router = makeRouter()
  await router.push(`/mes-recrutements/${RECRUTEMENT_UUID}`)

  let context!: ReturnType<typeof useCandidatures>

  mount(defineComponent({
    setup() {
      onSetup?.()
      context = useCandidatures()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada, router],
    },
  })

  return { context, router }
}

describe('useCandidatures', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockReset()
    vi.mocked(getCandidatureListe).mockReset()
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getCandidatureListe).mockResolvedValue(MOCK_LISTE)
  })

  describe('data', () => {
    it('computes totalCount from etapes', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.totalCount.value).toBe(3)
    })

    it('exposes error on api failure', async () => {
      vi.mocked(getRecrutementKanban).mockRejectedValue(new Error('API error'))

      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.error.value).toBeInstanceOf(Error)
    })

    it('moves a candidature between etapes', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const sourceColumnId = 'cccccccc-0001-0001-0001-000000000001'
      const targetColumnId = 'cccccccc-0001-0001-0001-000000000002'
      const cardId = 'dddddddd-0001-0001-0001-000000000001'

      context.moveCandidature({ sourceColumnId, targetColumnId, cardId })

      const sourceEtape = context.etapes.value.find(e => e.etape_uuid === sourceColumnId)
      const targetEtape = context.etapes.value.find(e => e.etape_uuid === targetColumnId)

      expect(sourceEtape?.candidatures).toHaveLength(1)
      expect(targetEtape?.candidatures).toHaveLength(2)
    })

    it('ignores move when source and target are the same', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const columnId = 'cccccccc-0001-0001-0001-000000000001'
      const cardId = 'dddddddd-0001-0001-0001-000000000001'
      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidature({ sourceColumnId: columnId, targetColumnId: columnId, cardId })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores move when source column is unknown', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidature({
        sourceColumnId: 'unknown-source',
        targetColumnId: 'cccccccc-0001-0001-0001-000000000002',
        cardId: 'dddddddd-0001-0001-0001-000000000001',
      })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores move when target column is unknown', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidature({
        sourceColumnId: 'cccccccc-0001-0001-0001-000000000001',
        targetColumnId: 'unknown-target',
        cardId: 'dddddddd-0001-0001-0001-000000000001',
      })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores move when card is not in source column', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidature({
        sourceColumnId: 'cccccccc-0001-0001-0001-000000000001',
        targetColumnId: 'cccccccc-0001-0001-0001-000000000002',
        cardId: 'unknown-card',
      })

      expect(context.etapes.value).toEqual(etapesBefore)
    })
  })

  describe('intitule', () => {
    it('exposes the intitule from the loaded detail', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.intitule.value).toBe('Chargé de mission numérique')
    })

    it('seeds the intitule from the recrutements list cache while pending', async () => {
      vi.mocked(getRecrutementKanban).mockImplementation(() => new Promise(() => {}))
      vi.mocked(getCandidatureListe).mockImplementation(() => new Promise(() => {}))

      const { context } = await mountCandidatures(() => {
        const queryCache = useQueryCache()
        queryCache.setQueryData(
          RECRUTEMENTS_QUERY_KEYS.actifs(ORGANISME_UUID),
          {
            count: 1,
            next: null,
            previous: null,
            results: [{ offer_id: RECRUTEMENT_UUID, intitule: 'Chargé de mission numérique' }],
          },
        )
      })

      expect(context.pending.value).toBe(true)
      expect(context.intitule.value).toBe('Chargé de mission numérique')
    })

    it('has no intitule while pending without cached list', async () => {
      vi.mocked(getRecrutementKanban).mockImplementation(() => new Promise(() => {}))

      const { context } = await mountCandidatures()

      expect(context.intitule.value).toBeNull()
    })
  })

  describe('filters', () => {
    it('exposes unfiltered data when no filter is active', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.filters.filteredEtapes.value).toHaveLength(2)
      expect(context.filters.filteredCandidatures.value).toHaveLength(3)
      expect(context.filters.activeFiltersCount.value).toBe(0)
    })

    it('filters kanban and liste by candidat name', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.search.value = 'alice dup'
      context.filters.flushSearch()

      const [reception, preselection] = context.filters.filteredEtapes.value
      expect(reception?.candidatures.map(c => c.candidat.nom)).toEqual(['Dupont'])
      expect(preselection?.candidatures).toHaveLength(0)
      expect(context.filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Dupont'])
    })

    it('filters kanban columns and liste rows by etape', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.draft.etapes = ['cccccccc-0001-0001-0001-000000000002']
      context.filters.apply()

      expect(context.filters.filteredEtapes.value.map(e => e.nom)).toEqual(['Présélection'])
      expect(context.filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Bernard'])
      expect(context.filters.activeFiltersCount.value).toBe(1)
    })

    it('combines etape filter and search', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.draft.etapes = ['cccccccc-0001-0001-0001-000000000001']
      context.filters.apply()
      context.filters.search.value = 'martin'
      context.filters.flushSearch()

      expect(context.filters.filteredEtapes.value).toHaveLength(1)
      expect(context.filters.filteredEtapes.value[0]?.candidatures.map(c => c.candidat.nom)).toEqual(['Martin'])
      expect(context.filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Martin'])
    })

    it('clears filters and search on reset', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.draft.etapes = ['cccccccc-0001-0001-0001-000000000002']
      context.filters.apply()
      context.filters.search.value = 'alice'
      context.filters.flushSearch()

      context.filters.reset()

      expect(context.filters.filteredEtapes.value).toHaveLength(2)
      expect(context.filters.filteredCandidatures.value).toHaveLength(3)
      expect(context.filters.search.value).toBe('')
      expect(context.filters.canReset.value).toBe(false)
    })
  })

  describe('shared instance', () => {
    it('shares the same state across components', async () => {
      const router = makeRouter()
      await router.push(`/mes-recrutements/${RECRUTEMENT_UUID}`)

      const contexts: ReturnType<typeof useCandidatures>[] = []

      const Child = defineComponent({
        setup() {
          contexts.push(useCandidatures())
          return () => h('div')
        },
      })

      mount(defineComponent({
        setup() {
          contexts.push(useCandidatures())
          return () => h(Child)
        },
      }), {
        global: {
          plugins: [createPinia(), PiniaColada, router],
        },
      })

      await vi.waitFor(() => expect(contexts[0]?.pending.value).toBe(false))

      expect(contexts[0]?.filters).toBe(contexts[1]?.filters)
      expect(contexts[0]?.recrutementUuid.value).toBe(RECRUTEMENT_UUID)
      expect(contexts[1]?.totalCount.value).toBe(3)
    })
  })

  describe('route changes', () => {
    it('resyncs etapes when the kanban data changes', async () => {
      let queryCache!: ReturnType<typeof useQueryCache>
      const { context } = await mountCandidatures(() => {
        queryCache = useQueryCache()
      })

      await vi.waitFor(() => expect(context.pending.value).toBe(false))
      expect(context.totalCount.value).toBe(3)

      queryCache.setQueryData(
        CANDIDATURES_QUERY_KEYS.kanban(ORGANISME_UUID, RECRUTEMENT_UUID),
        { ...MOCK_KANBAN, etapes: [MOCK_KANBAN.etapes[0]!] },
      )

      await vi.waitFor(() => expect(context.totalCount.value).toBe(2))
      expect(context.etapes.value).toHaveLength(1)
    })

    it('resets filters when navigating to another recrutement', async () => {
      const { context, router } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.search.value = 'alice'
      context.filters.flushSearch()
      context.filters.draft.etapes = ['cccccccc-0001-0001-0001-000000000001']
      context.filters.apply()
      expect(context.filters.activeFiltersCount.value).toBe(1)

      await router.push('/mes-recrutements/aaaaaaaa-0001-0001-0001-000000000002')

      await vi.waitFor(() => {
        expect(context.filters.search.value).toBe('')
        expect(context.filters.activeFiltersCount.value).toBe(0)
      })
      expect(context.recrutementUuid.value).toBe('aaaaaaaa-0001-0001-0001-000000000002')
    })
  })
})
