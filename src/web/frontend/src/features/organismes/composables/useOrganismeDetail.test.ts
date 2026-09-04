import type { OrganismeDetail } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { HttpError } from '@/api/errors'
import { useOrganismeDetail } from './useOrganismeDetail'

const mockGetOrganismeDetail = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: vi.fn(),
  getOrganismeDetail: (...args: unknown[]) => mockGetOrganismeDetail(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

const ORGANISME: OrganismeDetail = {
  organisme_uuid: ORGANISME_UUID,
  nom: 'Commune de Briançon',
  versant: 'FPT',
  siret: '21050023700354',
  gestionnaire: null,
  gestion_ats: true,
  date_creation: '2026-01-01',
  date_derniere_activite: '2026-01-15',
}

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountDetail() {
  let result!: ReturnType<typeof useOrganismeDetail>
  mount(defineComponent({
    setup() {
      result = useOrganismeDetail(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useOrganismeDetail', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetOrganismeDetail.mockResolvedValue(ORGANISME)
  })

  it('exposes the organisme detail', async () => {
    const { organisme, pending, notFound } = mountDetail()
    expect(pending.value).toBe(true)
    await flush()

    expect(mockGetOrganismeDetail).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(organisme.value).toEqual(ORGANISME)
    expect(notFound.value).toBe(false)
  })

  it('flags a 404 as not found', async () => {
    mockGetOrganismeDetail.mockRejectedValue(new HttpError(404, 'Not Found'))
    const { notFound } = mountDetail()
    await flush()

    expect(notFound.value).toBe(true)
  })

  it('does not flag other errors as not found', async () => {
    mockGetOrganismeDetail.mockRejectedValue(new HttpError(403, 'Forbidden'))
    const { notFound, error } = mountDetail()
    await flush()

    expect(notFound.value).toBe(false)
    expect(error.value).toBeInstanceOf(HttpError)
  })
})
