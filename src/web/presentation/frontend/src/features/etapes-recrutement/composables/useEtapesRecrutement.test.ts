import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
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

async function mountEtapes() {
  let result!: ReturnType<typeof useEtapesRecrutement>

  mount(defineComponent({
    setup() {
      result = useEtapesRecrutement(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })

  await vi.waitFor(() => expect(result.loading.value).toBe(false))

  return result
}

function lastUpdatePayload(): UpdateEtapeRecrutement[] {
  return mockUpdateEtapesRecrutement.mock.calls[0]![1] as UpdateEtapeRecrutement[]
}

describe('useEtapesRecrutement', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
    mockUpdateEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)
  })

  it('loads etapes on mount', async () => {
    const { etapes } = await mountEtapes()

    expect(mockGetEtapesRecrutement).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(etapes.value).toEqual(DEFAULT_ETAPES)
  })

  it('inserts new etape after the last EN_COURS without etape_uuid', async () => {
    const { addEtape } = await mountEtapes()
    await addEtape('Test technique')

    const payload = lastUpdatePayload()
    const refusIndex = payload.findIndex(p => p.categorie === 'REFUS')

    expect(payload).toHaveLength(DEFAULT_ETAPES.length + 1)
    expect(payload[refusIndex - 1]).toEqual({
      nom: 'Test technique',
      categorie: 'EN_COURS',
    })
  })

  it('removes etape by uuid and applies the server response', async () => {
    const freshEtapes = DEFAULT_ETAPES.filter(e => e.etape_uuid !== 'bbbb')
    mockUpdateEtapesRecrutement.mockResolvedValue(freshEtapes)

    const { etapes, removeEtape } = await mountEtapes()
    await removeEtape('bbbb')

    expect(etapes.value).toEqual(freshEtapes)
    const payload = lastUpdatePayload()
    expect(payload.find(p => p.etape_uuid === 'bbbb')).toBeUndefined()
  })

  it('inserts etape at specific index', async () => {
    const { addEtapeAt } = await mountEtapes()
    await addEtapeAt('Nouvelle', 2)

    const payload = lastUpdatePayload()
    expect(payload).toHaveLength(DEFAULT_ETAPES.length + 1)
    expect(payload[2]).toEqual({ nom: 'Nouvelle', categorie: 'EN_COURS' })
  })

  it('renames etape by uuid', async () => {
    const { renameEtape } = await mountEtapes()
    await renameEtape('bbbb', 'Présélection RH')

    const payload = lastUpdatePayload()
    const renamed = payload.find(p => p.etape_uuid === 'bbbb')
    expect(renamed?.nom).toBe('Présélection RH')
  })

  it('resets etapes to defaults', async () => {
    const customEtapes = DEFAULT_ETAPES.map(e => ({ ...e, nom: 'Custom' }))
    mockGetEtapesRecrutement.mockResolvedValue(customEtapes)
    mockInitEtapesRecrutement.mockResolvedValue(DEFAULT_ETAPES)

    const { etapes, resetEtapes } = await mountEtapes()
    await resetEtapes()

    expect(mockInitEtapesRecrutement).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(etapes.value).toEqual(DEFAULT_ETAPES)
  })

  it('exposes the mutation error without rejecting', async () => {
    mockUpdateEtapesRecrutement.mockRejectedValue(new Error('emulated API error'))

    const { error, etapes, renameEtape } = await mountEtapes()
    await renameEtape('bbbb', 'Présélection RH')

    expect(error.value).toBeInstanceOf(Error)
    expect(etapes.value).toEqual(DEFAULT_ETAPES)
  })

  it('locks etapes that are not EN_COURS', async () => {
    const { isEtapeLocked } = await mountEtapes()

    expect(isEtapeLocked(DEFAULT_ETAPES[1]!)).toBe(false)
    expect(isEtapeLocked(DEFAULT_ETAPES[0]!)).toBe(true)
    expect(isEtapeLocked(DEFAULT_ETAPES[3]!)).toBe(true)
  })

  it('reorders etapes by persisting the new order', async () => {
    const { reorderEtapes } = await mountEtapes()
    const reordered = [DEFAULT_ETAPES[2]!, DEFAULT_ETAPES[1]!, ...DEFAULT_ETAPES.slice(3)]
    await reorderEtapes([DEFAULT_ETAPES[0]!, ...reordered])

    const payload = lastUpdatePayload()
    expect(payload.map(p => p.etape_uuid)).toEqual(['aaaa', 'cccc', 'bbbb', 'dddd', 'eeee'])
  })

  it('appends a new etape at the end when there is no final etape', async () => {
    const etapesSansFinales = DEFAULT_ETAPES.slice(0, 3)
    mockGetEtapesRecrutement.mockResolvedValue(etapesSansFinales)

    const { addEtape } = await mountEtapes()
    await addEtape('Test technique')

    const payload = lastUpdatePayload()
    expect(payload).toHaveLength(etapesSansFinales.length + 1)
    expect(payload.at(-1)).toEqual({ nom: 'Test technique', categorie: 'EN_COURS' })
  })
})
