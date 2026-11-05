import type { Candidature, EtapeRecrutementDetailedCandidatures, RecrutementListe } from '../types'

export function groupCandidaturesByEtape({ etapes, results }: RecrutementListe): EtapeRecrutementDetailedCandidatures[] {
  const candidaturesByEtape = new Map<string, Candidature[]>(etapes.map(({ uuid }) => [uuid, []]))
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
  previousEtapes: EtapeRecrutementDetailedCandidatures[],
  etapes: EtapeRecrutementDetailedCandidatures[],
): Set<string> {
  const previousEtapeOf = new Map(previousEtapes.flatMap(etape =>
    etape.candidatures.map(({ uuid }) => [uuid, etape.uuid] as const)))

  return new Set(etapes
    .filter(etape => etape.candidatures.some(({ uuid }) =>
      previousEtapeOf.has(uuid) && previousEtapeOf.get(uuid) !== etape.uuid))
    .map(etape => etape.uuid))
}
