import type { OrganismeDetail, OrganismesList } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useOrganismes } from './useOrganismes'

const mockGetOrganismesPage = vi.fn()
const mockCreateOrganisme = vi.fn()
const mockUpdateOrganisme = vi.fn()

vi.mock('../api', () => ({
  getOrganismesPage: (...args: unknown[]) => mockGetOrganismesPage(...args),
  createOrganisme: (...args: unknown[]) => mockCreateOrganisme(...args),
  updateOrganisme: (...args: unknown[]) => mockUpdateOrganisme(...args),
}))

const ORGANISMES: OrganismesList[] = [
  {
    uuid: '11111111-1111-1111-1111-111111111111',
    nom: 'Organisme 1',
    siret: '11111111111111',
    superviseurs: '',
    gestion_ats: true,
    date_derniere_activite: '2026-08-01T00:00:00Z',
    date_creation: '2026-01-01T00:00:00Z',
    nombre_agents: 10,
    nombre_offres_publiees: 5,
    versant: 'FPT',
    authorized_actions: [],
  },
  {
    uuid: '22222222-2222-2222-2222-222222222222',
    nom: 'Organisme 2',
    siret: '22222222222222',
    superviseurs: 'Marie Noel',
    gestion_ats: false,
    date_derniere_activite: '2026-08-10T00:00:00Z',
    date_creation: '2026-02-01T00:00:00Z',
    nombre_agents: 5,
    nombre_offres_publiees: 2,
    versant: 'FPT',
    authorized_actions: [],
  },
]

const ORGANISMES_COUNT = 42

function pause(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

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
    mockGetOrganismesPage.mockResolvedValue({ count: ORGANISMES_COUNT, results: ORGANISMES })
  })

  it('exposes the first page and the total count', async () => {
    const { organismes, count, pending } = mountOrganismes()
    expect(pending.value).toBe(true)
    await flush()
    expect(pending.value).toBe(false)
    expect(mockGetOrganismesPage).toHaveBeenCalledWith({ page: 1, filter: undefined })
    expect(organismes.value).toEqual(ORGANISMES)
    expect(count.value).toBe(ORGANISMES_COUNT)
  })

  it('waits for three characters before filtering', async () => {
    const { search } = mountOrganismes()
    await flush()

    search.value = 'ma '
    await pause(400)

    expect(mockGetOrganismesPage).toHaveBeenCalledTimes(1)
  })

  it('filters with the trimmed term once typing pauses', async () => {
    const { search } = mountOrganismes()
    await flush()

    search.value = 'mai'
    await pause(100)
    search.value = ' mairie '

    await vi.waitFor(() => expect(mockGetOrganismesPage).toHaveBeenLastCalledWith({ page: 1, filter: 'mairie' }))
    expect(mockGetOrganismesPage).toHaveBeenCalledTimes(2)
  })

  it('goes back to the first page when the filter changes', async () => {
    const { page, search } = mountOrganismes()
    await flush()
    page.value = 3
    await flush()

    search.value = 'mairie'

    await vi.waitFor(() => expect(page.value).toBe(1))
    await flush()
    expect(mockGetOrganismesPage).toHaveBeenLastCalledWith({ page: 1, filter: 'mairie' })
    expect(mockGetOrganismesPage).not.toHaveBeenCalledWith({ page: 3, filter: 'mairie' })
  })

  it('keeps the current page displayed while the next one loads', async () => {
    const { page, organismes, pending } = mountOrganismes()
    await flush()
    mockGetOrganismesPage.mockReturnValue(new Promise(() => {}))

    page.value = 2
    await flush()

    expect(pending.value).toBe(false)
    expect(organismes.value).toEqual(ORGANISMES)
  })

  it('creates an organisme and refetches the list', async () => {
    const created: OrganismeDetail = {
      uuid: '33333333-3333-3333-3333-333333333333',
      nom: 'Organisme 3',
      siret: '33333333333333',
      superviseurs: '',
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
    expect(mockGetOrganismesPage).toHaveBeenCalledTimes(2)
  })

  it('updates an organisme and refetches the list', async () => {
    mockUpdateOrganisme.mockResolvedValue({ ...ORGANISMES[0], nom: 'Renommé' })
    const { update } = mountOrganismes()
    await flush()

    const payload = { nom: 'Renommé', versant: 'FPE' as const, gestion_ats: true }
    await update({ organismeUuid: ORGANISMES[0].uuid, payload })
    await flush()

    expect(mockUpdateOrganisme).toHaveBeenCalledWith(ORGANISMES[0].uuid, payload)
    expect(mockGetOrganismesPage).toHaveBeenCalledTimes(2)
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
