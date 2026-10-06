import type { PaginatedCandidatureListeList } from './types'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CANDIDAT_ALICE, ETAPE_RECEPTION } from '@/test/fixtures/candidatures'
import { getCandidatureListe } from './api'

function makeRow(index: number): PaginatedCandidatureListeList['results'][number] {
  return {
    uuid: `candidature-${index}`,
    date_soumission: '2025-06-10T09:15:00Z',
    date_derniere_activite: '2025-06-11T10:00:00Z',
    candidat: CANDIDAT_ALICE,
    etape: { uuid: ETAPE_RECEPTION, nom: 'Réception des candidatures', categorie: 'ENTREE' },
  }
}

const DEFAULT_PAGE_SIZE = 100

function serveListe(count: number) {
  vi.mocked(fetch).mockImplementation(async (input) => {
    const url = new URL((input as Request).url)
    const taille = Number(url.searchParams.get('taille') ?? DEFAULT_PAGE_SIZE)
    const results = Array.from({ length: Math.min(taille, count) }, (_, index) => makeRow(index))
    return Response.json({ count, next: null, previous: null, results })
  })
}

function requestedQueries(): string[] {
  return vi.mocked(fetch).mock.calls.map(([input]) => new URL((input as Request).url).search)
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('getCandidatureListe', () => {
  it('requests the whole liste in one page when the first page is incomplete', async () => {
    serveListe(250)

    const liste = await getCandidatureListe('organisme', 'recrutement')

    expect(requestedQueries()).toEqual(['', '?taille=250'])
    expect(liste.count).toBe(250)
    expect(liste.results.map(row => row.uuid)).toEqual(
      Array.from({ length: 250 }, (_, index) => `candidature-${index}`),
    )
  })

  it('requests a single page when the first page holds the whole liste', async () => {
    serveListe(42)

    const liste = await getCandidatureListe('organisme', 'recrutement')

    expect(requestedQueries()).toEqual([''])
    expect(liste.results).toHaveLength(42)
  })
})
