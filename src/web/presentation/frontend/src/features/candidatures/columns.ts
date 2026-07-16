import type { CandidatureListe } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import ElapsedDaysCell from '@/features/recrutements/components/cells/ElapsedDaysCell.vue'
import EtapeRecrutementCell from './components/cells/EtapeRecrutementCell.vue'
import { formatCandidatName } from './format'

export const CANDIDATURE_LISTE_COLUMNS: CspColumnDef<CandidatureListe>[] = [
  { id: 'candidat', header: 'Candidat', accessor: row => formatCandidatName(row.candidat) },
  { id: 'etape', header: 'Étape', accessor: row => row.etape.nom, cellComponent: EtapeRecrutementCell },
  { id: 'date_soumission', header: 'Date candidature', sortable: true, accessor: row => row.date_soumission, cellComponent: ElapsedDaysCell },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
]
