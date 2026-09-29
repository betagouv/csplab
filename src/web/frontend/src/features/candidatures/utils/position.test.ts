import type { EtapeRecrutementDetailedCandidatures } from '../types'
import { describe, expect, it } from 'vitest'
import { findEtapeOfCandidature, findPositionInList } from './position'

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
      etape: { etape_uuid: etapeUuid, nom: etapeUuid, categorie: 'EN_COURS' },
    })),
  }
}

const ETAPES = [etape('entree', ['a']), etape('entretien', ['b', 'c', 'd'])]
const SEQUENCE = ETAPES.flatMap(({ candidatures }) => candidatures)

describe('findPositionInList', () => {
  it('locates a candidature in the displayed order, across the etapes', () => {
    expect(findPositionInList(SEQUENCE, 'b')).toEqual({ index: 1, total: 4, previousUuid: 'a', nextUuid: 'c' })
  })

  it('has no neighbour before the first nor after the last', () => {
    expect(findPositionInList(SEQUENCE, 'a')).toMatchObject({ previousUuid: null, nextUuid: 'b' })
    expect(findPositionInList(SEQUENCE, 'd')).toMatchObject({ previousUuid: 'c', nextUuid: null })
  })

  it('returns an unknown position for a candidature absent from the display', () => {
    expect(findPositionInList(SEQUENCE, 'masquee')).toBeNull()
  })
})

describe('findEtapeOfCandidature', () => {
  it('returns the column holding the candidature', () => {
    expect(findEtapeOfCandidature(ETAPES, 'c')?.etape_uuid).toBe('entretien')
    expect(findEtapeOfCandidature(ETAPES, 'masquee')).toBeNull()
  })
})
