import type { Candidature, RecrutementDetailKanban } from '../types'

export function moveCandidaturesInKanban(
  kanban: RecrutementDetailKanban,
  candidatureUuids: string[],
  targetEtapeUuid: string,
): RecrutementDetailKanban {
  if (!kanban.etapes.some(etape => etape.uuid === targetEtapeUuid)) {
    return kanban
  }

  const movable = new Map<string, Candidature>(kanban.etapes
    .filter(etape => etape.uuid !== targetEtapeUuid)
    .flatMap(etape => etape.candidatures.map(candidature => [candidature.uuid, candidature] as const)))
  const moved = candidatureUuids.flatMap(uuid => movable.get(uuid) ?? [])

  if (moved.length === 0) {
    return kanban
  }

  const movedUuids = new Set(moved.map(candidature => candidature.uuid))
  return {
    ...kanban,
    etapes: kanban.etapes.map(etape => etape.uuid === targetEtapeUuid
      ? { ...etape, candidatures: [...etape.candidatures, ...moved] }
      : { ...etape, candidatures: etape.candidatures.filter(candidature => !movedUuids.has(candidature.uuid)) }),
  }
}
