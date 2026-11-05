import type { EtapeRecrutementDetailedCandidatures, RecrutementDetailKanban, RecrutementListe } from '../types'
import { describe, expect, it } from 'vitest'
import { kanbanColumns } from '@/test/fixtures/candidatures'
import { etapesReceivingCandidatures, groupCandidaturesByEtape, moveCandidaturesInKanban } from './kanban'

function etape(etapeUuid: string, candidatureUuids: string[]): EtapeRecrutementDetailedCandidatures {
  return {
    uuid: etapeUuid,
    nom: etapeUuid,
    categorie: 'EN_COURS',
    candidatures: candidatureUuids.map(uuid => ({
      uuid,
      date_soumission: '2025-06-10T09:15:00Z',
      date_derniere_activite: '2025-06-10T09:15:00Z',
      unread_conversations: 0,
      candidat: { uuid: `candidat-${uuid}`, nom: uuid, prenom: uuid },
    })),
  }
}

const KANBAN: RecrutementDetailKanban = {
  uuid: 'recrutement',
  etapes: [etape('entree', ['a', 'b']), etape('entretien', ['c']), etape('refus', ['d'])],
}

function liste(rows: [candidatureUuid: string, etapeUuid: string][], etapeUuids: string[]): RecrutementListe {
  return {
    count: rows.length,
    next: null,
    previous: null,
    results: rows.map(([uuid, etapeUuid]) => ({
      uuid,
      date_soumission: '2025-06-10T09:15:00Z',
      date_derniere_activite: '2025-06-10T09:15:00Z',
      unread_conversations: 0,
      candidat: { uuid: `candidat-${uuid}`, nom: uuid, prenom: uuid },
      etape: { uuid: etapeUuid, nom: etapeUuid, categorie: 'EN_COURS' },
    })),
    etapes: etapeUuids.map(uuid => ({ uuid, nom: uuid, categorie: 'EN_COURS' })),
  }
}

function columns(etapes: EtapeRecrutementDetailedCandidatures[]): [string, string[]][] {
  return etapes.map(({ uuid, candidatures }) => [uuid, candidatures.map(candidature => candidature.uuid)])
}

describe('groupCandidaturesByEtape', () => {
  it('lays out every etape in the order of the recrutement, empty ones included, keeping the order of the liste', () => {
    const grouped = groupCandidaturesByEtape(liste(
      [['c', 'refus'], ['a', 'entree'], ['b', 'refus']],
      ['entree', 'entretien', 'refus'],
    ))

    expect(columns(grouped)).toEqual([
      ['entree', ['a']],
      ['entretien', []],
      ['refus', ['c', 'b']],
    ])
  })

  it('ignores candidatures whose etape is not part of the recrutement', () => {
    const grouped = groupCandidaturesByEtape(liste([['a', 'supprimee']], ['entree']))

    expect(columns(grouped)).toEqual([['entree', []]])
  })
})

describe('moveCandidaturesInKanban', () => {
  it('appends the candidatures to the target column in the given order, from any source column', () => {
    expect(kanbanColumns(moveCandidaturesInKanban(KANBAN, ['d', 'b'], 'entretien'))).toEqual({
      entree: ['a'],
      entretien: ['c', 'd', 'b'],
      refus: [],
    })
  })

  it.each([
    { when: 'the target column is unknown', uuids: ['a'], target: 'inconnue' },
    { when: 'the candidatures are unknown', uuids: ['inconnue'], target: 'entretien' },
    { when: 'the candidatures are already in the target column', uuids: ['c'], target: 'entretien' },
  ])('returns the kanban unchanged when $when', ({ uuids, target }) => {
    expect(moveCandidaturesInKanban(KANBAN, uuids, target)).toBe(KANBAN)
  })
})

describe('etapesReceivingCandidatures', () => {
  it('returns the columns a candidature moved into', () => {
    const before = [etape('entree', ['a', 'b']), etape('entretien', ['c']), etape('refus', [])]
    const after = [etape('entree', ['a']), etape('entretien', ['c']), etape('refus', ['b'])]

    expect(etapesReceivingCandidatures(before, after)).toEqual(new Set(['refus']))
  })

  it('ignores candidatures shown again once a filter is removed', () => {
    const filtered = [etape('entree', ['a']), etape('entretien', [])]
    const unfiltered = [etape('entree', ['a', 'b']), etape('entretien', ['c'])]

    expect(etapesReceivingCandidatures(filtered, unfiltered)).toEqual(new Set())
  })
})
