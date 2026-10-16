import type { Candidat, CandidatureDetail } from './types'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import { formatElapsedDays } from '@/utils/date'

export function formatCandidatName(candidat: Candidat): string {
  return `${candidat.prenom} ${candidat.nom}`.trim()
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
