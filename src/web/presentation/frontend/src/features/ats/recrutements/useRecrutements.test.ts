import type { RecrutementsQuery } from '../api/recrutement'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutements } from '../api/recrutement'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from './mock'
import { useRecrutements } from './useRecrutements'

vi.mock('../api/recrutement', () => ({
  getRecrutements: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

function mockApiWithFixtures(): void {
  vi.mocked(getRecrutements).mockImplementation(
    async (_organismeUuid: string, query: RecrutementsQuery = {}) => {
      const results = query.filtre === 'archives' ? RECRUTEMENTS_ARCHIVES : RECRUTEMENTS_ACTIFS
      return { count: results.length, next: null, previous: null, results }
    },
  )
}

describe('useRecrutements', () => {
  beforeEach(() => {
    vi.mocked(getRecrutements).mockReset()
    mockApiWithFixtures()
  })

  it('loads actifs and archives offres on success', async () => {
    const { state, error, data, load } = useRecrutements(ORGANISME_UUID)
    await load()
    expect(state.value).toBe('success')
    expect(error.value).toBeNull()
    expect(data.actifs).toEqual(RECRUTEMENTS_ACTIFS)
    expect(data.archives).toEqual(RECRUTEMENTS_ARCHIVES)
  })

  it('queries actifs and archives for the given organisme', async () => {
    const { load } = useRecrutements(ORGANISME_UUID)
    await load()
    expect(getRecrutements).toHaveBeenCalledWith(
      ORGANISME_UUID,
      expect.objectContaining({ filtre: 'actifs' }),
    )
    expect(getRecrutements).toHaveBeenCalledWith(
      ORGANISME_UUID,
      expect.objectContaining({ filtre: 'archives' }),
    )
  })

  it('handles api error', async () => {
    vi.mocked(getRecrutements).mockRejectedValue(new Error('emulated API error'))
    const { state, error, data, load } = useRecrutements(ORGANISME_UUID)
    void load()
    await vi.waitFor(() => expect(state.value).toBe('error'))
    expect(error.value).toBeInstanceOf(Error)
    expect(data.actifs).toEqual([])
  })
})
