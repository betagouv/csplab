import type { components } from '@/types/api'

export type EtapeFixture = components['schemas']['EtapeRecrutement']

export const RECEPTION: EtapeFixture = { uuid: 'ffffffff-0001-0001-0001-000000000001', nom: 'Réception', categorie: 'ENTREE' }
export const PRESELECTION: EtapeFixture = { uuid: 'ffffffff-0001-0001-0001-000000000002', nom: 'Présélection', categorie: 'EN_COURS' }
export const ENTRETIEN: EtapeFixture = { uuid: 'ffffffff-0001-0001-0001-000000000003', nom: 'Entretien', categorie: 'EN_COURS' }
export const REFUS: EtapeFixture = { uuid: 'ffffffff-0001-0001-0001-000000000004', nom: 'Refus', categorie: 'REFUS' }
export const RECRUTEMENT: EtapeFixture = { uuid: 'ffffffff-0001-0001-0001-000000000005', nom: 'Recrutement', categorie: 'ACCEPTE' }

export const ETAPES: EtapeFixture[] = [RECEPTION, PRESELECTION, ENTRETIEN, REFUS, RECRUTEMENT]

export const ETAPES_RENAMED: EtapeFixture[] = ETAPES.map(etape => etape === PRESELECTION ? { ...etape, nom: 'Présélection RH' } : etape)
