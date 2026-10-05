import type { PaginatedCandidatureListeList, RecrutementDetailKanban } from '../types'
import type { Utilisateur } from '@/api/utilisateur'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { RECRUTEMENTS_QUERY_KEYS } from '@/features/recrutements/queries'
import { routes } from '@/router'
import { getCandidatureListe, getRecrutementKanban } from '../api'
import { CANDIDATURES_QUERY_KEYS } from '../queries'
import { useCandidatures } from './useCandidatures'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

const MOCK_USER: Utilisateur = {
  email: 'marie.dupont@example.gouv.fr',
  prenom: 'Marie',
  nom: 'Dupont',
  is_staff: false,
  organisme_roles: [{ organisme_uuid: ORGANISME_UUID, nom: 'Mairie de Paris', role: 'agent' }],
}
const ETAPE_RECEPTION = 'cccccccc-0001-0001-0001-000000000001'
const ETAPE_PRESELECTION = 'cccccccc-0001-0001-0001-000000000002'
const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'

const MOCK_DETAIL: RecrutementDetail = {
  uuid: RECRUTEMENT_UUID,
  intitule: 'Chargé de mission numérique',
  archive: false,
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
    { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
    { uuid: ETAPE_PRESELECTION, nom: 'Présélection', categorie: 'EN_COURS' },
  ],
}

const MOCK_KANBAN: RecrutementDetailKanban = {
  uuid: RECRUTEMENT_UUID,
  etapes: [
    {
      uuid: 'cccccccc-0001-0001-0001-000000000001',
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
      uuid: 'cccccccc-0001-0001-0001-000000000002',
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
      etape: { uuid: 'cccccccc-0001-0001-0001-000000000001', nom: 'Réception des candidatures', categorie: 'ENTREE' },
    },
    {
      uuid: 'dddddddd-0001-0001-0001-000000000002',
      date_soumission: '2025-06-11T14:30:00Z',
      date_derniere_activite: '2025-06-12T09:15:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' },
      etape: { uuid: 'cccccccc-0001-0001-0001-000000000001', nom: 'Réception des candidatures', categorie: 'ENTREE' },
    },
    {
      uuid: 'dddddddd-0001-0001-0001-000000000005',
      date_soumission: '2025-06-08T10:00:00Z',
      date_derniere_activite: '2025-06-11T10:00:00Z',
      candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000005', nom: 'Bernard', prenom: 'Élise' },
      etape: { uuid: 'cccccccc-0001-0001-0001-000000000002', nom: 'Présélection', categorie: 'EN_COURS' },
    },
  ],
}

function makeRouter() {
  return createRouter({ history: createMemoryHistory(), routes })
}

async function mountCandidatures(
  onSetup?: () => void,
  path = `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`,
) {
  const router = makeRouter()
  await router.push(path)

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
    vi.mocked(getMe).mockReset()
    vi.mocked(getRecrutementDetail).mockReset()
    vi.mocked(getRecrutementKanban).mockReset()
    vi.mocked(getCandidatureListe).mockReset()
    vi.mocked(getMe).mockResolvedValue(MOCK_USER)
    vi.mocked(getRecrutementDetail).mockResolvedValue(MOCK_DETAIL)
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getCandidatureListe).mockResolvedValue(MOCK_LISTE)
  })

  describe('data', () => {
    it('computes totalCount from etapes', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))

      expect(context.totalCount.value).toBe(3)
    })

    it('loads the kanban behind an opened candidature', async () => {
      const { context } = await mountCandidatures(
        undefined,
        `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/candidatures/${CANDIDATURE_ALICE}`,
      )

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))

      expect(getRecrutementKanban).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
      expect(context.totalCount.value).toBe(3)
    })

    it('exposes error on api failure', async () => {
      vi.mocked(getRecrutementKanban).mockRejectedValue(new Error('API error'))

      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))

      expect(context.error.value).toBeInstanceOf(Error)
    })
  })

  describe('intitule', () => {
    it('exposes the intitule from the loaded detail', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pendingDetail.value).toBe(false))

      expect(context.intitule.value).toBe('Chargé de mission numérique')
    })

    it('seeds the intitule from the recrutements list cache while pending', async () => {
      vi.mocked(getRecrutementDetail).mockImplementation(() => new Promise(() => {}))

      const { context } = await mountCandidatures(() => {
        const queryCache = useQueryCache()
        queryCache.setQueryData(
          RECRUTEMENTS_QUERY_KEYS.actifs(ORGANISME_UUID),
          {
            count: 1,
            next: null,
            previous: null,
            results: [{ uuid: RECRUTEMENT_UUID, intitule: 'Chargé de mission numérique' }],
          },
        )
      })

      await vi.waitFor(() =>
        expect(context.intitule.value).toBe('Chargé de mission numérique'),
      )
      expect(context.pendingDetail.value).toBe(true)
    })

    it('has no intitule while pending without cached list', async () => {
      vi.mocked(getRecrutementDetail).mockImplementation(() => new Promise(() => {}))

      const { context } = await mountCandidatures()

      expect(context.intitule.value).toBeNull()
    })
  })

  describe('filters', () => {
    // La logique des filtres est couverte en isolation dans
    // useCandidaturesFilters.test.ts ; ici on vérifie seulement le câblage sur
    // les données live de la query.
    it('applies filters to the live kanban data', async () => {
      const { context } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))

      context.filters.draft.etapes = [ETAPE_PRESELECTION]
      context.filters.apply()

      expect(context.filters.filteredEtapes.value.map(e => e.nom)).toEqual(['Présélection'])
    })

    it('applies filters to the live liste data', async () => {
      const { context } = await mountCandidatures(
        undefined,
        `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/liste`,
      )

      await vi.waitFor(() => expect(context.pendingListe.value).toBe(false))

      context.filters.draft.etapes = [ETAPE_PRESELECTION]
      context.filters.apply()

      expect(context.filters.filteredCandidatures.value.map(c => c.candidat.nom)).toEqual(['Bernard'])
    })
  })

  describe('shared instance', () => {
    it('shares the same state across components', async () => {
      const router = makeRouter()
      await router.push(`/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`)

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

      await vi.waitFor(() => expect(contexts[0]?.pendingKanban.value).toBe(false))

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

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))
      expect(context.totalCount.value).toBe(3)

      queryCache.setQueryData(
        CANDIDATURES_QUERY_KEYS.kanban(ORGANISME_UUID, RECRUTEMENT_UUID),
        { ...MOCK_KANBAN, etapes: [MOCK_KANBAN.etapes[0]!] },
      )

      await vi.waitFor(() => expect(context.totalCount.value).toBe(2))
      expect(context.candidatureKanban.value).toHaveLength(1)
    })

    it('resets filters when navigating to another recrutement', async () => {
      const { context, router } = await mountCandidatures()

      await vi.waitFor(() => expect(context.pendingKanban.value).toBe(false))

      context.filters.search.value = 'alice'
      context.filters.flushSearch()
      context.filters.draft.etapes = [ETAPE_RECEPTION]
      context.filters.apply()
      expect(context.filters.activeFiltersCount.value).toBe(1)

      await router.push(`/organismes/${ORGANISME_UUID}/recrutements/aaaaaaaa-0001-0001-0001-000000000002`)

      await vi.waitFor(() => {
        expect(context.filters.search.value).toBe('')
        expect(context.filters.activeFiltersCount.value).toBe(0)
      })
      expect(context.recrutementUuid.value).toBe('aaaaaaaa-0001-0001-0001-000000000002')
    })
  })
})
