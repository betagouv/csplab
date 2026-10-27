import type { CandidatureListe } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import BadgeCell from '@/components/base/CspDataTable/cells/BadgeCell.vue'
import ElapsedDaysCell from '@/components/base/CspDataTable/cells/ElapsedDaysCell.vue'
import CandidatNomCell from './components/cells/CandidatNomCell.vue'
import { formatCandidatName } from './format'

export const CANDIDATURE_LISTE_COLUMNS: CspColumnDef<CandidatureListe>[] = [
  { id: 'candidat', header: 'Candidat', accessor: row => formatCandidatName(row.candidat), cellComponent: CandidatNomCell },
  { id: 'etape', header: 'Étape', accessor: row => row.etape.nom, cellComponent: BadgeCell },
  { id: 'date_soumission', header: 'Date candidature', sortable: true, accessor: row => row.date_soumission, cellComponent: ElapsedDaysCell },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
]
