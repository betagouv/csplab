export interface CandidaturePosition {
  index: number
  total: number
  previousUuid: string | null
  nextUuid: string | null
}

export function findCandidaturePosition(sequence: string[], candidatureUuid: string): CandidaturePosition | null {
  const index = sequence.indexOf(candidatureUuid)
  if (index === -1) {
    return null
  }
  return {
    index,
    total: sequence.length,
    previousUuid: sequence[index - 1] ?? null,
    nextUuid: sequence[index + 1] ?? null,
  }
}
