import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ORGANISME } from '@/test/fixtures/organismes'
import { getOrganismesPage } from './api'
import { ORGANISMES_PAGE_SIZE } from './constants/organisme'

function serveOrganismes(count: number) {
  vi.mocked(fetch).mockImplementation(async (input) => {
    const url = new URL((input as Request).url)
    const page = Number(url.searchParams.get('page') ?? 1)
    const taille = Number(url.searchParams.get('taille'))
    const start = (page - 1) * taille
    const results = Array.from(
      { length: Math.max(0, Math.min(taille, count - start)) },
      (_, index) => ({ ...ORGANISME, uuid: `organisme-${start + index}` }),
    )
    return Response.json({ count, next: null, previous: null, results })
  })
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('getOrganismesPage', () => {
  it('requests the page and the filter with the organismes page size', async () => {
    serveOrganismes(250)

    const page = await getOrganismesPage({ page: 2, filter: 'mairie' })

    const url = new URL((vi.mocked(fetch).mock.calls[0]![0] as Request).url)
    expect(Object.fromEntries(url.searchParams)).toEqual({
      page: '2',
      taille: String(ORGANISMES_PAGE_SIZE),
      filter: 'mairie',
    })
    expect(page.count).toBe(250)
    expect(page.results).toHaveLength(250 - ORGANISMES_PAGE_SIZE)
  })
})
