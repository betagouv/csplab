import type { EtapeRecrutement } from '@/features/etapes-recrutement/types'

export const ETAPES_RECRUTEMENT: EtapeRecrutement[] = [
  { uuid: 'aaaa', nom: 'Réception', categorie: 'ENTREE' },
  { uuid: 'bbbb', nom: 'Présélection', categorie: 'EN_COURS' },
  { uuid: 'cccc', nom: 'Entretien', categorie: 'EN_COURS' },
  { uuid: 'dddd', nom: 'Refus', categorie: 'REFUS' },
  { uuid: 'eeee', nom: 'Recrutement', categorie: 'ACCEPTE' },
]
