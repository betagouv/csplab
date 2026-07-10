import type { CandidatureListe, RecrutementDetailKanban } from './types'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { formatDateLong } from '@/utils/date'

export function formatCandidatName(candidat: CandidatureListe['candidat']): string {
  return `${candidat.prenom} ${candidat.nom}`
}

export function formatRecrutementMeta(detail: RecrutementDetailKanban): CspMetaItem[] {
  return [
    {
      icon: 'ri:calendar-line',
      srLabel: 'Date de création',
      label: `Créé le ${formatDateLong(detail.date_publication)}`,
    },
    {
      icon: 'ri:map-pin-2-line',
      srLabel: 'Localisation',
      label: detail.localisation.localisation_label,
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
