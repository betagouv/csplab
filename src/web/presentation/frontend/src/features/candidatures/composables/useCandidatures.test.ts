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
const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
const ETAPE_PRESELECTION = 'cccccccc-0001-0001-0001-000000000002'
const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'

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

      context.moveCandidature({
        sourceColumnId: ETAPE_RECEPTION,
        targetColumnId: ETAPE_PRESELECTION,
        cardId: CANDIDATURE_ALICE,
      })

      const source = context.etapes.value.find(e => e.etape_uuid === ETAPE_RECEPTION)
      const target = context.etapes.value.find(e => e.etape_uuid === ETAPE_PRESELECTION)

      expect(source?.candidatures).toHaveLength(1)
      expect(target?.candidatures).toHaveLength(2)
    })

    it.each([
      { when: 'source and target are the same', sourceColumnId: ETAPE_RECEPTION, targetColumnId: ETAPE_RECEPTION, cardId: CANDIDATURE_ALICE },
      { when: 'the source column is unknown', sourceColumnId: 'unknown', targetColumnId: ETAPE_PRESELECTION, cardId: CANDIDATURE_ALICE },
      { when: 'the target column is unknown', sourceColumnId: ETAPE_RECEPTION, targetColumnId: 'unknown', cardId: CANDIDATURE_ALICE },
      { when: 'the card is not in the source column', sourceColumnId: ETAPE_RECEPTION, targetColumnId: ETAPE_PRESELECTION, cardId: 'unknown' },
    ])('leaves etapes untouched when $when', async ({ sourceColumnId, targetColumnId, cardId }) => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const before = structuredClone(context.etapes.value)
      context.moveCandidature({ sourceColumnId, targetColumnId, cardId })

      expect(context.etapes.value).toEqual(before)
    })

    it('leaves etapes empty when the kanban data is not loaded', async () => {
      vi.mocked(getRecrutementKanban).mockImplementation(() => new Promise(() => {}))

      const { context } = await mountCandidatures()

      context.moveCandidature({
        sourceColumnId: ETAPE_RECEPTION,
        targetColumnId: ETAPE_PRESELECTION,
        cardId: CANDIDATURE_ALICE,
      })

      expect(context.etapes.value).toEqual([])
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

  describe('moveCandidaturesBatch', () => {
    it('moves multiple candidatures between etapes in batch', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const sourceColumnId = ETAPE_RECEPTION
      const targetColumnId = ETAPE_PRESELECTION

      const candidaturesByEtape = new Map([
        [sourceColumnId, ['dddddddd-0001-0001-0001-000000000001', 'dddddddd-0001-0001-0001-000000000002']],
      ])

      context.moveCandidaturesBatch({ candidaturesByEtape, targetColumnId })

      const sourceEtape = context.etapes.value.find(etape => etape.etape_uuid === sourceColumnId)
      const targetEtape = context.etapes.value.find(etape => etape.etape_uuid === targetColumnId)

      expect(sourceEtape?.candidatures).toHaveLength(0)
      expect(targetEtape?.candidatures).toHaveLength(3)
    })

    it('ignores batch move when target column is unknown', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const etapesBefore = structuredClone(context.etapes.value)

      const candidaturesByEtape = new Map([
        [ETAPE_RECEPTION, ['dddddddd-0001-0001-0001-000000000001']],
      ])

      context.moveCandidaturesBatch({ candidaturesByEtape, targetColumnId: 'unknown-target' })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores batch move when source column is unknown', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const etapesBefore = structuredClone(context.etapes.value)

      const candidaturesByEtape = new Map([
        ['unknown-source', ['dddddddd-0001-0001-0001-000000000001']],
      ])

      context.moveCandidaturesBatch({
        candidaturesByEtape,
        targetColumnId: ETAPE_PRESELECTION,
      })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores candidatures from same column as target in batch move', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const targetColumnId = ETAPE_PRESELECTION

      const candidaturesByEtape = new Map([
        [targetColumnId, ['dddddddd-0001-0001-0001-000000000005']],
      ])

      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidaturesBatch({ candidaturesByEtape, targetColumnId })

      expect(context.etapes.value).toEqual(etapesBefore)
    })

    it('ignores unknown candidatures in batch move', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      const sourceColumnId = ETAPE_RECEPTION
      const targetColumnId = ETAPE_PRESELECTION

      const candidaturesByEtape = new Map([
        [sourceColumnId, ['unknown-card-1', 'unknown-card-2']],
      ])

      const etapesBefore = structuredClone(context.etapes.value)

      context.moveCandidaturesBatch({ candidaturesByEtape, targetColumnId })

      expect(context.etapes.value).toEqual(etapesBefore)
    })
  })

  describe('filters', () => {
    // La logique des filtres est couverte en isolation dans
    // useCandidaturesFilters.test.ts ; ici on vérifie seulement le câblage sur
    // les données live de la query.
    it('applies filters to the live kanban and liste data', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      context.filters.draft.etapes = [ETAPE_PRESELECTION]
      context.filters.apply()

      expect(context.filters.filteredEtapes.value.map(e => e.nom)).toEqual(['Présélection'])
      expect(context.filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Bernard'])
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
      context.filters.draft.etapes = [ETAPE_RECEPTION]
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
