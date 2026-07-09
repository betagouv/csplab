import type { RecrutementDetailKanban } from '../types'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutementKanban } from '../api'
import { useCandidaturesKanban } from './useCandidaturesKanban'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
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

describe('useCandidaturesKanban', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockReset()
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
  })

  it('loads kanban from the api', async () => {
    const { kanban, load, pending } = useCandidaturesKanban(ORGANISME_UUID, RECRUTEMENT_UUID)
    await load()

    expect(getRecrutementKanban).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
    expect(kanban.value).toEqual(MOCK_KANBAN)
    expect(pending.value).toBe(false)
  })

  it('computes totalCount across etapes', async () => {
    const { totalCount, load } = useCandidaturesKanban(ORGANISME_UUID, RECRUTEMENT_UUID)
    await load()

    expect(totalCount.value).toBe(3)
  })

  it('exposes etapes from kanban data', async () => {
    const { etapes, load } = useCandidaturesKanban(ORGANISME_UUID, RECRUTEMENT_UUID)
    await load()

    expect(etapes.value).toHaveLength(2)
    expect(etapes.value[0]?.nom).toBe('Réception des candidatures')
  })

  it('stores the error on api failure', async () => {
    vi.mocked(getRecrutementKanban).mockRejectedValue(new Error('emulated API error'))

    const { error, kanban, load } = useCandidaturesKanban(ORGANISME_UUID, RECRUTEMENT_UUID)
    await load()

    expect(error.value).toBeInstanceOf(Error)
    expect(kanban.value).toBeNull()
  })
})
