import type { OrganismeDetail, OrganismesList } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useOrganismes } from './useOrganismes'

const mockGetOrganismesList = vi.fn()
const mockCreateOrganisme = vi.fn()
const mockUpdateOrganisme = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: (...args: unknown[]) => mockGetOrganismesList(...args),
  createOrganisme: (...args: unknown[]) => mockCreateOrganisme(...args),
  updateOrganisme: (...args: unknown[]) => mockUpdateOrganisme(...args),
}))

const ORGANISMES: OrganismesList[] = [
  {
    organisme_uuid: '11111111-1111-1111-1111-111111111111',
    nom: 'Organisme 1',
    siret: '11111111111111',
    gestionnaire: null,
    gestion_ats: true,
    date_derniere_activite: '2026-08-01T00:00:00Z',
    date_creation: '2026-01-01T00:00:00Z',
    nombre_agents: 10,
    nombre_offres_publiees: 5,
    versant: 'FPT',
  },
  {
    organisme_uuid: '22222222-2222-2222-2222-222222222222',
    nom: 'Organisme 2',
    siret: '22222222222222',
    gestionnaire: 'Marie Noel',
    gestion_ats: false,
    date_derniere_activite: '2026-08-10T00:00:00Z',
    date_creation: '2026-02-01T00:00:00Z',
    nombre_agents: 5,
    nombre_offres_publiees: 2,
    versant: 'FPT',
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
    mockGetOrganismesList.mockResolvedValue(ORGANISMES)
  })

  it('exposes the organismes list', async () => {
    const { organismesList, pending } = mountOrganismes()
    expect(pending.value).toBe(true)
    await flush()
    expect(pending.value).toBe(false)
    expect(organismesList.value).toEqual(ORGANISMES)
  })

  it('creates an organisme and refetches the list', async () => {
    const created: OrganismeDetail = {
      organisme_uuid: '33333333-3333-3333-3333-333333333333',
      nom: 'Organisme 3',
      siret: '33333333333333',
      gestionnaire: null,
      gestion_ats: true,
      date_derniere_activite: '2026-08-19T00:00:00Z',
      date_creation: '2026-08-19T00:00:00Z',
      versant: 'FPH',
    }
    mockCreateOrganisme.mockResolvedValue(created)
    const { create } = mountOrganismes()
    await flush()

    await create({
      nom: 'Organisme 3',
      siret: '33333333333333',
      versant: 'FPH',
      gestion_ats: true,
    })
    await flush()

    expect(mockCreateOrganisme).toHaveBeenCalledWith({
      nom: 'Organisme 3',
      siret: '33333333333333',
      versant: 'FPH',
      gestion_ats: true,
    })
    expect(mockGetOrganismesList).toHaveBeenCalledTimes(2)
  })

  it('updates an organisme and refetches the list', async () => {
    mockUpdateOrganisme.mockResolvedValue({ ...ORGANISMES[0], nom: 'Renommé' })
    const { update } = mountOrganismes()
    await flush()

    const payload = { nom: 'Renommé', versant: 'FPE' as const, gestion_ats: true }
    await update({ organismeUuid: ORGANISMES[0].organisme_uuid, payload })
    await flush()

    expect(mockUpdateOrganisme).toHaveBeenCalledWith(ORGANISMES[0].organisme_uuid, payload)
    expect(mockGetOrganismesList).toHaveBeenCalledTimes(2)
  })

  it('propagates creation errors to the caller', async () => {
    mockCreateOrganisme.mockRejectedValue(new Error('boom'))
    const { create } = mountOrganismes()
    await flush()

    await expect(create({
      nom: 'X',
      siret: '44444444444444',
      versant: 'FPE',
      gestion_ats: true,
    })).rejects.toThrow('boom')
  })
})
