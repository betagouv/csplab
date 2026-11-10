import type { RecrutementRole } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

export const RECRUTEMENT_ROLE_LABELS: Record<RecrutementRole, string> = {
  responsable: 'Responsable',
  recruteur: 'Recruteur',
  contributeur: 'Contributeur',
}

const RECRUTEMENT_ROLE_HINTS: Record<RecrutementRole, string> = {
  responsable: 'Pilote ce recrutement. Il configure les étapes de recrutement, constitue l\'équipe et dispose de tous les droits sur le traitement des candidatures.',
  recruteur: 'Participe au recrutement. Il peut faire avancer les candidatures, communiquer avec les candidats et gérer le processus de recrutement.',
  contributeur: 'Contribue au recrutement. Il peut consulter les candidatures et rédiger des notes.',
}

export const RECRUTEMENT_ROLE_OPTIONS: (CspRadioGroupOption & { value: RecrutementRole })[] = (
  Object.keys(RECRUTEMENT_ROLE_LABELS) as RecrutementRole[]
).map(role => ({ value: role, label: RECRUTEMENT_ROLE_LABELS[role], hint: RECRUTEMENT_ROLE_HINTS[role] }))
