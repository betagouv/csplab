import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { HttpError } from '@/api/errors'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { useOrganismeDetail } from './useOrganismeDetail'

const mockGetOrganismeDetail = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: (...args: unknown[]) => mockGetOrganismeDetail(...args),
}))

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountDetail() {
  let result!: ReturnType<typeof useOrganismeDetail>
  mount(defineComponent({
    setup() {
      result = useOrganismeDetail(ORGANISME_DETAIL.uuid)
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
    mockGetOrganismeDetail.mockResolvedValue(ORGANISME_DETAIL)
  })

  it('exposes the organisme detail', async () => {
    const { organisme, pending, notFound } = mountDetail()
    expect(pending.value).toBe(true)
    await flush()

    expect(mockGetOrganismeDetail).toHaveBeenCalledWith(ORGANISME_DETAIL.uuid)
    expect(organisme.value).toEqual(ORGANISME_DETAIL)
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
