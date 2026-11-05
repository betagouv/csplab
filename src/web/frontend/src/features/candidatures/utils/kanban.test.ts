import type { KanbanColumn, RecrutementListe } from '../types'
import { describe, expect, it } from 'vitest'
import { etapesReceivingCandidatures, groupCandidaturesByEtape } from './kanban'

function etape(etapeUuid: string, candidatureUuids: string[]): KanbanColumn {
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

function columns(etapes: KanbanColumn[]): [string, string[]][] {
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
