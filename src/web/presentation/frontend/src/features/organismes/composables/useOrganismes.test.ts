import type { OrganismeAdmin } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useOrganismes } from './useOrganismes'

const mockGetOrganismes = vi.fn()
const mockCreateOrganisme = vi.fn()
const mockUpdateOrganisme = vi.fn()

vi.mock('../api', () => ({
  getOrganismes: (...args: unknown[]) => mockGetOrganismes(...args),
  createOrganisme: (...args: unknown[]) => mockCreateOrganisme(...args),
  updateOrganisme: (...args: unknown[]) => mockUpdateOrganisme(...args),
}))

const ORGANISMES: OrganismeAdmin[] = [
  {
    uuid: '11111111-1111-1111-1111-111111111111',
    nom: 'Organisme 1',
    siret: '11111111111111',
    versant: 'FPE',
    gestion_candidatures: true,
    gestionnaire: null,
  },
  {
    uuid: '22222222-2222-2222-2222-222222222222',
    nom: 'Organisme 2',
    siret: '22222222222222',
    versant: 'FPT',
    gestion_candidatures: false,
    gestionnaire: { prenom: 'Marie', nom: 'Noel' },
  },
]

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountOrganismes() {
  let result!: ReturnType<typeof useOrganismes>
  mount(defineComponent({
    setup() {
      result = useOrganismes()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useOrganismes', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetOrganismes.mockResolvedValue(ORGANISMES)
  })

  it('exposes the organismes list', async () => {
    const { organismes, pending } = mountOrganismes()
    expect(pending.value).toBe(true)
    await flush()
    expect(pending.value).toBe(false)
    expect(organismes.value).toEqual(ORGANISMES)
  })

  it('creates an organisme and refetches the list', async () => {
    const created: OrganismeAdmin = {
      uuid: '33333333-3333-3333-3333-333333333333',
      nom: 'Organisme 3',
      siret: '33333333333333',
      versant: 'FPH',
      gestion_candidatures: true,
      gestionnaire: null,
    }
    mockCreateOrganisme.mockResolvedValue(created)
    const { create } = mountOrganismes()
    await flush()

    await create({
      nom: 'Organisme 3',
      siret: '33333333333333',
      versant: 'FPH',
      gestion_candidatures: true,
    })
    await flush()

    expect(mockCreateOrganisme).toHaveBeenCalledWith({
      nom: 'Organisme 3',
      siret: '33333333333333',
      versant: 'FPH',
      gestion_candidatures: true,
    })
    expect(mockGetOrganismes).toHaveBeenCalledTimes(2)
  })

  it('updates an organisme and refetches the list', async () => {
    mockUpdateOrganisme.mockResolvedValue({ ...ORGANISMES[0], nom: 'Renommé' })
    const { update } = mountOrganismes()
    await flush()

    await update({
      uuid: ORGANISMES[0].uuid,
      payload: { nom: 'Renommé', versant: 'FPE', gestion_candidatures: true },
    })
    await flush()

    expect(mockUpdateOrganisme).toHaveBeenCalledWith(ORGANISMES[0].uuid, {
      nom: 'Renommé',
      versant: 'FPE',
      gestion_candidatures: true,
    })
    expect(mockGetOrganismes).toHaveBeenCalledTimes(2)
  })

  it('propagates creation errors to the caller', async () => {
    mockCreateOrganisme.mockRejectedValue(new Error('boom'))
    const { create } = mountOrganismes()
    await flush()

    await expect(create({
      nom: 'X',
      siret: '44444444444444',
      versant: 'FPE',
      gestion_candidatures: true,
    })).rejects.toThrow('boom')
  })
})
