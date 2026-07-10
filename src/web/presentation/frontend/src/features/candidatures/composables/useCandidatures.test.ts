import type { PaginatedCandidatureListeResponse, RecrutementDetailKanban } from '../types'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getCandidatureListe, getRecrutementKanban } from '../api'
import { provideCandidatures, useCandidatures } from './useCandidatures'

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

const MOCK_LISTE: PaginatedCandidatureListeResponse = {
  count: 3,
  next: null,
  previous: null,
  results: [],
}

describe('useCandidatures', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockReset()
    vi.mocked(getCandidatureListe).mockReset()
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getCandidatureListe).mockResolvedValue(MOCK_LISTE)
  })

  describe('provideCandidatures', () => {
    it('computes totalCount from etapes', async () => {
      const context = provideCandidatures(ORGANISME_UUID, RECRUTEMENT_UUID)

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.totalCount.value).toBe(3)
    })

    it('exposes error on api failure', async () => {
      vi.mocked(getRecrutementKanban).mockRejectedValue(new Error('API error'))

      const context = provideCandidatures(ORGANISME_UUID, RECRUTEMENT_UUID)

      await vi.waitFor(() => expect(context.pending.value).toBe(false))

      expect(context.error.value).toBeInstanceOf(Error)
    })

    it('moves a candidature between etapes', async () => {
      const context = provideCandidatures(ORGANISME_UUID, RECRUTEMENT_UUID)

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
  })

  describe('useCandidatures', () => {
    it('throws if called outside provider', () => {
      expect(() => useCandidatures()).toThrow('useCandidatures must be used within CandidaturesView')
    })
  })
})
