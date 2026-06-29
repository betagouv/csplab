import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../api/recrutement'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useEtapesRecrutement } from './useEtapesRecrutement'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000001'

const mockGetEtapesRecrutement = vi.fn()
const mockUpdateEtapesRecrutement = vi.fn()

vi.mock('../api/recrutement', () => ({
  getEtapesRecrutement: (...args: unknown[]) => mockGetEtapesRecrutement(...args),
  updateEtapesRecrutement: (...args: unknown[]) => mockUpdateEtapesRecrutement(...args),
}))

const DEFAULT_ETAPES: EtapeRecrutement[] = [
  { etape_uuid: 'aaaa', nom: 'Réception', categorie: 'ENTREE' },
  { etape_uuid: 'bbbb', nom: 'Présélection', categorie: 'EN_COURS' },
  { etape_uuid: 'cccc', nom: 'Entretien', categorie: 'EN_COURS' },
  { etape_uuid: 'dddd', nom: 'Refus', categorie: 'REFUS' },
  { etape_uuid: 'eeee', nom: 'Recrutement', categorie: 'ACCEPTE' },
]

describe('useEtapesRecrutement', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches etapes and toggles loading', async () => {
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { etapes, loading, fetchEtapes } = useEtapesRecrutement(ORGANISME_UUID)
    const promise = fetchEtapes()
    expect(loading.value).toBe(true)
    await promise

    expect(loading.value).toBe(false)
    expect(etapes.value).toEqual(DEFAULT_ETAPES)
    expect(mockGetEtapesRecrutement).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('inserts new etape after the last EN_COURS without etape_uuid', async () => {
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
    mockUpdateEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { fetchEtapes, addEtape } = useEtapesRecrutement(ORGANISME_UUID)
    await fetchEtapes()
    await addEtape()

    const payload = mockUpdateEtapesRecrutement.mock.calls[0][1] as UpdateEtapeRecrutement[]
    const refusIndex = payload.findIndex(p => p.categorie === 'REFUS')

    expect(payload).toHaveLength(DEFAULT_ETAPES.length + 1)
    expect(payload[refusIndex - 1]).toEqual({
      nom: 'Nouvelle étape',
      categorie: 'EN_COURS',
    })
  })

  it('removes etape by uuid', async () => {
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
    mockUpdateEtapesRecrutement.mockResolvedValue(
      DEFAULT_ETAPES.filter(e => e.etape_uuid !== 'bbbb'),
    )

    const { etapes, fetchEtapes, removeEtape } = useEtapesRecrutement(ORGANISME_UUID)
    await fetchEtapes()
    await removeEtape('bbbb')

    expect(etapes.value.find(e => e.etape_uuid === 'bbbb')).toBeUndefined()
    const payload = mockUpdateEtapesRecrutement.mock.calls[0][1] as UpdateEtapeRecrutement[]
    expect(payload.find(p => p.etape_uuid === 'bbbb')).toBeUndefined()
  })
})
