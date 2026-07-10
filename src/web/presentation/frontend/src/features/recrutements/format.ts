import type {
  RecrutementBase,
  TypeContrat,
} from './types'

export const TYPE_CONTRAT_LABELS = {
  TITULAIRE_CONTRACTUEL: 'Titulaire et contractuel',
  CONTRACTUELS: 'Contractuels',
  TERRITORIAL: 'Territorial',
} satisfies Record<TypeContrat, string>

export function formatResponsablesLabel(row: RecrutementBase): string {
  return row.responsables.map(r => r.nom).join(', ') || '-'
}
