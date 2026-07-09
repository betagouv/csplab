import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '../mock'
import { useRecrutements } from './useRecrutements'

vi.mock('../api', () => ({
  getRecrutementsActifs: vi.fn(),
  getRecrutementsArchives: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

function buildPaginatedResponse<T>(results: T[]) {
  return { count: results.length, next: null, previous: null, results }
}

describe('useRecrutements', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementsActifs).mockReset()
    vi.mocked(getRecrutementsArchives).mockReset()
    vi.mocked(getRecrutementsActifs).mockResolvedValue(buildPaginatedResponse(RECRUTEMENTS_ACTIFS))
    vi.mocked(getRecrutementsArchives).mockResolvedValue(buildPaginatedResponse(RECRUTEMENTS_ARCHIVES))
  })

  it('loads actifs from the api', async () => {
    const { data, load, pending } = useRecrutements(ORGANISME_UUID)
    await load()

    expect(getRecrutementsActifs).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(data.actifs).toEqual(RECRUTEMENTS_ACTIFS)
    expect(pending.value).toBe(false)
  })

  it('loads archives on demand', async () => {
    const { data, load } = useRecrutements(ORGANISME_UUID)
    await load('archives')

    expect(getRecrutementsArchives).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(data.archives).toEqual(RECRUTEMENTS_ARCHIVES)
  })

  it('tracks loaded state per tab with has()', async () => {
    const { has, load } = useRecrutements(ORGANISME_UUID)
    expect(has('actifs')).toBe(false)

    await load('actifs')
    expect(has('actifs')).toBe(true)
    expect(has('archives')).toBe(false)
  })

  it('stores the error on api failure', async () => {
    vi.mocked(getRecrutementsActifs).mockRejectedValue(new Error('emulated API error'))

    const { error, data, load } = useRecrutements(ORGANISME_UUID)
    await load()

    expect(error.value).toBeInstanceOf(Error)
    expect(data.actifs).toEqual([])
  })
})
