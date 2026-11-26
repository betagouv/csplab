import type { EtapeRecrutement } from '@/features/etapes-recrutement/types'

export const RECEPTION: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000001', nom: 'Réception', categorie: 'ENTREE' }
export const PRESELECTION: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000002', nom: 'Présélection', categorie: 'EN_COURS' }
export const ENTRETIEN: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000003', nom: 'Entretien', categorie: 'EN_COURS' }
export const REFUS: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000004', nom: 'Refus', categorie: 'REFUS' }
export const RECRUTEMENT: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000005', nom: 'Recrutement', categorie: 'ACCEPTE' }

export const ETAPES: EtapeRecrutement[] = [RECEPTION, PRESELECTION, ENTRETIEN, REFUS, RECRUTEMENT]

export const ETAPES_RENAMED: EtapeRecrutement[] = ETAPES.map(etape => etape === PRESELECTION ? { ...etape, nom: 'Présélection RH' } : etape)
