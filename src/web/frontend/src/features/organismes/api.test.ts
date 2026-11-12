import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import { ORGANISME } from '@/test/fixtures/organismes'
import { getOrganismesList, getOrganismesPage } from './api'

const BACK_MAX_PAGE_SIZE = 1_000

function serveOrganismes(count: number) {
  vi.mocked(fetch).mockImplementation(async (input) => {
    const url = new URL((input as Request).url)
    const page = Number(url.searchParams.get('page') ?? 1)
    const taille = Math.min(Number(url.searchParams.get('taille') ?? 100), BACK_MAX_PAGE_SIZE)
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

describe('getOrganismesList', () => {
  it('gathers every organisme beyond the page size limit of the back', async () => {
    serveOrganismes(2345)

    const organismes = await getOrganismesList()

    expect(organismes.map(organisme => organisme.uuid)).toEqual(
      Array.from({ length: 2345 }, (_, index) => `organisme-${index}`),
    )
  })

  it('requests a single page when it holds every organisme', async () => {
    serveOrganismes(42)

    const organismes = await getOrganismesList()

    expect(fetch).toHaveBeenCalledTimes(1)
    expect(organismes).toHaveLength(42)
  })
})

describe('getOrganismesPage', () => {
  it('requests the page and the filter with the table page size', async () => {
    serveOrganismes(42)

    const page = await getOrganismesPage({ page: 2, filter: 'mairie' })

    const url = new URL((vi.mocked(fetch).mock.calls[0]![0] as Request).url)
    expect(Object.fromEntries(url.searchParams)).toEqual({
      page: '2',
      taille: String(TABLE_PAGE_SIZE),
      filter: 'mairie',
    })
    expect(page.count).toBe(42)
    expect(page.results).toHaveLength(42 - TABLE_PAGE_SIZE)
  })
})
