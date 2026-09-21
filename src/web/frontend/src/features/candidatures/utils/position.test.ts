import type { EtapeRecrutementDetailedCandidatures } from '../types'
import { describe, expect, it } from 'vitest'
import { findCandidaturePosition, findEtapeOfCandidature } from './position'

function etape(etapeUuid: string, candidatureUuids: string[]): EtapeRecrutementDetailedCandidatures {
  return {
    etape_uuid: etapeUuid,
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

const ETAPES = [etape('entree', ['a']), etape('entretien', ['b', 'c', 'd'])]

describe('findCandidaturePosition', () => {
  it('locates a candidature within its own column, in display order', () => {
    expect(findCandidaturePosition(ETAPES, 'c')).toEqual({ index: 1, total: 3, previousUuid: 'b', nextUuid: 'd' })
  })

  it('has no neighbour before the first nor after the last of the column', () => {
    expect(findCandidaturePosition(ETAPES, 'b')).toMatchObject({ previousUuid: null, nextUuid: 'c' })
    expect(findCandidaturePosition(ETAPES, 'd')).toMatchObject({ previousUuid: 'c', nextUuid: null })
  })

  it('returns an unknown position for a candidature absent from the displayed columns', () => {
    expect(findCandidaturePosition(ETAPES, 'masquee')).toBeNull()
  })
})

describe('findEtapeOfCandidature', () => {
  it('returns the column holding the candidature', () => {
    expect(findEtapeOfCandidature(ETAPES, 'c')?.etape_uuid).toBe('entretien')
    expect(findEtapeOfCandidature(ETAPES, 'masquee')).toBeNull()
  })
})
