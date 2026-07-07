import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api/recrutement'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from './mock'
import { useRecrutements } from './useRecrutements'

vi.mock('../api/recrutement', () => ({
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

  it('loads actifs from mocks when mock source is enabled', async () => {
    const { state, error, data, load } = useRecrutements({ source: 'mock' })
    await load()

    expect(state.value).toBe('success')
    expect(error.value).toBeNull()
    expect(data.actifs).toEqual(RECRUTEMENTS_ACTIFS)
    expect(data.archives).toEqual([])
    expect(getRecrutementsActifs).not.toHaveBeenCalled()
  })

  it('loads archives from mocks on demand', async () => {
    const { data, load } = useRecrutements({ source: 'mock' })
    await load('archives')

    expect(data.archives).toEqual(RECRUTEMENTS_ARCHIVES)
    expect(getRecrutementsArchives).not.toHaveBeenCalled()
  })

  it('calls the api in api mode', async () => {
    const { load } = useRecrutements({ organismeUuid: ORGANISME_UUID, source: 'api' })
    await load()

    expect(getRecrutementsActifs).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('handles api error', async () => {
    vi.mocked(getRecrutementsActifs).mockRejectedValue(new Error('emulated API error'))

    const { state, error, data, load } = useRecrutements({ organismeUuid: ORGANISME_UUID, source: 'api' })
    void load()

    await vi.waitFor(() => expect(state.value).toBe('error'))
    expect(error.value).toBeInstanceOf(Error)
    expect(data.actifs).toEqual([])
  })
})
