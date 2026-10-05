import type { EtapeRecrutementDetailedCandidatures, RecrutementDetailKanban } from '../types'
import { describe, expect, it } from 'vitest'
import { kanbanColumns } from '@/test/fixtures/candidatures'
import { moveCandidaturesInKanban } from './kanban'

function etape(etapeUuid: string, candidatureUuids: string[]): EtapeRecrutementDetailedCandidatures {
  return {
    uuid: etapeUuid,
    nom: etapeUuid,
    categorie: 'EN_COURS',
    candidatures: candidatureUuids.map(uuid => ({
      uuid,
      date_soumission: '2025-06-10T09:15:00Z',
      date_derniere_activite: '2025-06-10T09:15:00Z',
      candidat: { uuid: `candidat-${uuid}`, nom: uuid, prenom: uuid },
    })),
  }
}

const KANBAN: RecrutementDetailKanban = {
  uuid: 'recrutement',
  etapes: [etape('entree', ['a', 'b']), etape('entretien', ['c']), etape('refus', ['d'])],
}

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
