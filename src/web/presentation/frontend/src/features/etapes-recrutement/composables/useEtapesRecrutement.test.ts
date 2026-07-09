import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useEtapesRecrutement } from './useEtapesRecrutement'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000001'

const mockGetEtapesRecrutement = vi.fn()
const mockUpdateEtapesRecrutement = vi.fn()
const mockInitEtapesRecrutement = vi.fn()

vi.mock('../api', () => ({
  getEtapesRecrutement: (...args: unknown[]) => mockGetEtapesRecrutement(...args),
  updateEtapesRecrutement: (...args: unknown[]) => mockUpdateEtapesRecrutement(...args),
  initEtapesRecrutement: (...args: unknown[]) => mockInitEtapesRecrutement(...args),
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
    await addEtape('Test technique')

    const payload = mockUpdateEtapesRecrutement.mock.calls[0][1] as UpdateEtapeRecrutement[]
    const refusIndex = payload.findIndex(p => p.categorie === 'REFUS')

    expect(payload).toHaveLength(DEFAULT_ETAPES.length + 1)
    expect(payload[refusIndex - 1]).toEqual({
      nom: 'Test technique',
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

  it('inserts etape at specific index', async () => {
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
    mockUpdateEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { fetchEtapes, addEtapeAt } = useEtapesRecrutement(ORGANISME_UUID)
    await fetchEtapes()
    await addEtapeAt('Nouvelle', 2)

    const payload = mockUpdateEtapesRecrutement.mock.calls[0][1] as UpdateEtapeRecrutement[]
    expect(payload).toHaveLength(DEFAULT_ETAPES.length + 1)
    expect(payload[2]).toEqual({ nom: 'Nouvelle', categorie: 'EN_COURS' })
  })

  it('renames etape by uuid', async () => {
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
    mockUpdateEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { fetchEtapes, renameEtape } = useEtapesRecrutement(ORGANISME_UUID)
    await fetchEtapes()
    await renameEtape('bbbb', 'Présélection RH')

    const payload = mockUpdateEtapesRecrutement.mock.calls[0][1] as UpdateEtapeRecrutement[]
    const renamed = payload.find(p => p.etape_uuid === 'bbbb')
    expect(renamed?.nom).toBe('Présélection RH')
  })

  it('resets etapes to defaults', async () => {
    const customEtapes = DEFAULT_ETAPES.map(e => ({ ...e, nom: 'Custom' }))
    mockGetEtapesRecrutement.mockResolvedValue(customEtapes)
    mockInitEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { etapes, fetchEtapes, resetEtapes } = useEtapesRecrutement(ORGANISME_UUID)
    await fetchEtapes()
    await resetEtapes()

    expect(mockInitEtapesRecrutement).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(etapes.value).toEqual(DEFAULT_ETAPES)
  })
})
