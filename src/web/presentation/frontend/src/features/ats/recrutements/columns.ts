import type { RecrutementActif, RecrutementArchive, RecrutementBase } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import CandidaturesCell from './components/cells/CandidaturesCell.vue'
import ElapsedDaysCell from './components/cells/ElapsedDaysCell.vue'
import OffreActionsCell from './components/cells/OffreActionsCell.vue'
import OffreIntituleCell from './components/cells/OffreIntituleCell.vue'
import { formatTypeOffre } from './format'

export function responsablesLabel(row: RecrutementBase): string {
  return row.responsables.map(r => r.nom).join(', ') || '-'
}

export const RECRUTEMENTS_ACTIFS_COLUMNS: CspColumnDef<RecrutementActif>[] = [
  { id: 'intitule', header: 'Intitulé de l’offre', accessor: row => row.intitule, cellComponent: OffreIntituleCell },
  { id: 'reference_csp', header: 'Référence CSP', accessor: row => row.reference_csp },
  { id: 'date_publication', header: 'Publication', sortable: true, accessor: row => row.date_publication, cellComponent: ElapsedDaysCell },
  { id: 'responsables', header: 'Responsable', sortable: true, accessor: responsablesLabel },
  { id: 'type', header: 'Type', sortable: true, accessor: row => formatTypeOffre(row.type_contrat, row.kind_contrat) },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'candidatures', header: 'Candidatures actives', accessor: row => row.candidatures?.total ?? null, cellComponent: CandidaturesCell },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]

export const RECRUTEMENTS_ARCHIVES_COLUMNS: CspColumnDef<RecrutementArchive>[] = [
  { id: 'intitule', header: 'Intitulé de l’offre', accessor: row => row.intitule, cellComponent: OffreIntituleCell },
  { id: 'reference_csp', header: 'Référence CSP', accessor: row => row.reference_csp },
  { id: 'responsables', header: 'Responsable', sortable: true, accessor: responsablesLabel },
  { id: 'type', header: 'Type', sortable: true, accessor: row => formatTypeOffre(row.type_contrat, row.kind_contrat) },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'finalise', header: 'Finalisée', sortable: true, accessor: row => (row.finalise ? 'Oui' : 'Non') },
  { id: 'recrute', header: 'Recruté', accessor: row => row.recrute },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]
