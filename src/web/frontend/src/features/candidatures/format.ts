import type { CandidatureDetail, CandidatureListe } from './types'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { formatDateLong, formatElapsedDays } from '@/utils/date'

export function formatCandidatName(candidat: CandidatureListe['candidat']): string {
  return `${candidat.prenom} ${candidat.nom}`
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

export function formatCandidatureMeta(detail: CandidatureDetail): CspMetaItem[] {
  return [
    {
      icon: 'ri:calendar-line',
      srLabel: 'Date de candidature',
      label: `Candidature ${formatElapsedDays(detail.date_candidature)}`,
    },
    {
      icon: 'ri:mail-line',
      srLabel: 'Courriel',
      label: detail.candidat.email,
      copy: { action: 'Copier le courriel', confirmation: 'Courriel copié dans le presse-papier' },
    },
  ]
}
