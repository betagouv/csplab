import type { KanbanCard, KanbanColumn, RecrutementListe } from '../types'

export function groupCandidaturesByEtape({ etapes, results }: RecrutementListe): KanbanColumn[] {
  const candidaturesByEtape = new Map<string, KanbanCard[]>(etapes.map(({ uuid }) => [uuid, []]))
  for (const row of results) {
    candidaturesByEtape.get(row.etape.uuid)?.push(row)
  }
  return etapes.map(({ uuid, nom, categorie }) => ({
    uuid,
    nom,
    categorie,
    candidatures: candidaturesByEtape.get(uuid)!,
  }))
}

export function etapesReceivingCandidatures(
  previousEtapes: KanbanColumn[],
  etapes: KanbanColumn[],
): Set<string> {
  const previousEtapeOf = new Map(previousEtapes.flatMap(etape =>
    etape.candidatures.map(({ uuid }) => [uuid, etape.uuid] as const)))

  return new Set(etapes
    .filter(etape => etape.candidatures.some(({ uuid }) =>
      previousEtapeOf.has(uuid) && previousEtapeOf.get(uuid) !== etape.uuid))
    .map(etape => etape.uuid))
}
