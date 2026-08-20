import type { OrganismesList } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useOrganismes } from './useOrganismes'

const mockGetOrganismes = vi.fn()

vi.mock('../api', () => ({
  getOrganismes: (...args: unknown[]) => mockGetOrganismes(...args),
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
    mockGetOrganismes.mockResolvedValue(ORGANISMES)
  })

  it('exposes the organismes list', async () => {
    const { organismes, pending } = mountOrganismes()
    expect(pending.value).toBe(true)
    await flush()
    expect(pending.value).toBe(false)
    expect(organismes.value).toEqual(ORGANISMES)
  })
})
