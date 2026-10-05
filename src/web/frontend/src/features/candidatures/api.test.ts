import type { PaginatedCandidatureListeList } from './types'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { getCandidatureListe } from './api'

function makeRow(index: number): PaginatedCandidatureListeList['results'][number] {
  return {
    uuid: `candidature-${index}`,
    date_soumission: '2025-06-10T09:15:00Z',
    date_derniere_activite: '2025-06-11T10:00:00Z',
    candidat: { uuid: `candidat-${index}`, nom: 'Dupont', prenom: 'Alice' },
    etape: { uuid: 'etape-reception', nom: 'Réception des candidatures', categorie: 'ENTREE' },
  }
}

function serveListe(count: number) {
  vi.mocked(fetch).mockImplementation(async (input) => {
    const url = new URL((input as Request).url)
    const page = Number(url.searchParams.get('page'))
    const taille = Number(url.searchParams.get('taille'))
    const from = (page - 1) * taille
    const results = Array.from({ length: Math.max(0, Math.min(taille, count - from)) }, (_, index) => makeRow(from + index))
    return Response.json({ count, next: null, previous: null, results })
  })
}

function requestedPages(): string[] {
  return vi.mocked(fetch).mock.calls.map(([input]) => new URL((input as Request).url).search)
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('getCandidatureListe', () => {
  it('loads every page of the liste', async () => {
    serveListe(250)

    const liste = await getCandidatureListe('organisme', 'recrutement')

    expect(requestedPages()).toEqual(['?page=1&taille=100', '?page=2&taille=100', '?page=3&taille=100'])
    expect(liste.count).toBe(250)
    expect(liste.next).toBeNull()
    expect(liste.results.map(row => row.uuid)).toEqual(
      Array.from({ length: 250 }, (_, index) => `candidature-${index}`),
    )
  })

  it('requests a single page when the liste is empty', async () => {
    serveListe(0)

    const liste = await getCandidatureListe('organisme', 'recrutement')

    expect(requestedPages()).toEqual(['?page=1&taille=100'])
    expect(liste.results).toEqual([])
  })
})
