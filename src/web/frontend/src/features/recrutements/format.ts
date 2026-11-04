import type {
  NatureOffre,
  RecrutementBase,
  RecrutementDetail,
} from './types'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { formatDateLong } from '@/utils/date'

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

export function formatLocalisationLabel(detail: RecrutementDetail): string {
  const [principale, ...autres] = detail.localisations
  if (!principale) {
    return '-'
  }
  return autres.length
    ? `${principale.localisation_label} + ${autres.length}`
    : principale.localisation_label
}

export function formatRecrutementMeta(detail: RecrutementDetail): CspMetaItem[] {
  return [
    {
      icon: 'ri:calendar-line',
      srLabel: 'Date de création',
      label: `Créé le ${formatDateLong(detail.date_publication)}`,
    },
    {
      icon: 'ri:map-pin-2-line',
      srLabel: 'Localisation',
      label: formatLocalisationLabel(detail),
    },
    {
      icon: 'ri:government-line',
      srLabel: 'Organisme',
      label: detail.organisme_recruteur.nom,
    },
    {
      icon: 'ri:price-tag-3-line',
      srLabel: 'Catégorie',
      label: `Catégorie ${detail.categorie_offre}`,
    },
  ]
}
