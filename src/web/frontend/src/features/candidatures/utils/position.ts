import type { CandidatureListe, EtapeRecrutementDetailedCandidatures } from '../types'

export interface CandidaturePosition {
  index: number
  total: number
  previousUuid: string | null
  nextUuid: string | null
}

export function findPositionInList(
  candidatures: CandidatureListe[],
  candidatureUuid: string,
): CandidaturePosition | null {
  const uuids = candidatures.map(candidature => candidature.uuid)
  const index = uuids.indexOf(candidatureUuid)
  if (index === -1) {
    return null
  }
  return {
    index,
    total: uuids.length,
    previousUuid: uuids[index - 1] ?? null,
    nextUuid: uuids[index + 1] ?? null,
  }
}

export function findEtapeOfCandidature(
  etapes: EtapeRecrutementDetailedCandidatures[],
  candidatureUuid: string,
): EtapeRecrutementDetailedCandidatures | null {
  return etapes.find(etape => etape.candidatures.some(candidature => candidature.uuid === candidatureUuid)) ?? null
}
