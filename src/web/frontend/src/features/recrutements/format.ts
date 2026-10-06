import type {
  NatureOffre,
  RecrutementBase,
} from './types'

export const NATURE_OFFRE_LABELS = {
  TITULAIRE_CONTRACTUEL: 'Titulaire et contractuel',
  CONTRACTUEL: 'Contractuels',
  TERRITORIAL: 'Territorial',
} satisfies Record<NatureOffre, string>

export function formatResponsablesLabel(row: RecrutementBase): string {
  return row.responsables.map(r => r.nom).join(', ') || '-'
}

export function formatNatureOffreLabel(row: RecrutementBase): string {
  return row.nature_offre ? NATURE_OFFRE_LABELS[row.nature_offre] : '-'
}
