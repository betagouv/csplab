import type { KindContrat, TypeContrat } from './types'

export const TYPE_CONTRAT_LABELS = {
  TITULAIRE_CONTRACTUEL: 'Titulaire et contractuel',
  CONTRACTUELS: 'Contractuels',
  TERRITORIAL: 'Territorial',
} satisfies Record<TypeContrat, string>

export const KIND_CONTRAT_LABELS = {
  CDD: 'CDD',
  CDI: 'CDI',
  PERMANENT: 'Permanent',
  VACATION: 'Vacation',
  STAGE: 'Stage',
} satisfies Record<KindContrat, string>

export function formatTypeOffre(
  typeContrat: TypeContrat | null,
  kindContrat: KindContrat | null,
): string {
  const parts = [
    typeContrat ? TYPE_CONTRAT_LABELS[typeContrat] : null,
    kindContrat ? KIND_CONTRAT_LABELS[kindContrat] : null,
  ].filter((p): p is string => Boolean(p))
  return parts.join(' · ') || '-'
}
