import type { Candidat, CandidatureDetail, EtapeRecrutement } from './types'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { formatElapsedDays } from '@/utils/date'
import { formatPersonName } from '@/utils/format'

export function formatCandidatName(candidat: Candidat): string {
  return formatPersonName(candidat)
}

export function formatEtapeChangeTitle(candidats: Candidat[], etapeNom: string): string {
  const [candidat] = candidats
  if (candidats.length === 1 && candidat) {
    const name = formatCandidatName(candidat)
    const preposition = /^[aeiouyhàâéèêëîïôûü]/i.test(name) ? 'd\'' : 'de '
    return `La candidature ${preposition}${name} est passée à l'étape ${etapeNom}`
  }
  return `${candidats.length} candidatures sont passées à l'étape ${etapeNom}`
}

export function etapeOptions(etapes: EtapeRecrutement[], currentEtapeUuid: string): CspRadioGroupOption[] {
  return etapes.map((etape) => {
    const isCurrent = etape.uuid === currentEtapeUuid
    return {
      value: etape.uuid,
      label: etape.nom,
      hint: isCurrent ? 'Étape actuelle' : undefined,
      disabled: isCurrent,
    }
  })
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
    },
  ]
}
