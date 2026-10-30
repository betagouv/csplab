import type { RecrutementsActifs, RecrutementsArchives } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import BadgeCell from '@/components/base/CspDataTable/cells/BadgeCell.vue'
import ElapsedDaysCell from '@/components/base/CspDataTable/cells/ElapsedDaysCell.vue'
import OffreActionsCell from './components/cells/OffreActionsCell.vue'
import OffreIntituleCell from './components/cells/OffreIntituleCell.vue'
import { formatNatureOffreLabel, formatResponsablesLabel } from './format'

export const RECRUTEMENTS_ACTIFS_COLUMNS: CspColumnDef<RecrutementsActifs>[] = [
  { id: 'intitule', header: 'Intitulé du recrutement', accessor: row => row.intitule, cellComponent: OffreIntituleCell },
  { id: 'reference_csp', header: 'Référence CSP', accessor: row => row.reference_csp },
  { id: 'date_publication', header: 'Publication', sortable: true, accessor: row => row.date_publication, cellComponent: ElapsedDaysCell },
  { id: 'responsables', header: 'Responsable', sortable: true, accessor: formatResponsablesLabel },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'total', header: 'Nombre total de candidatures', width: '8.5rem', wrapHeader: true, accessor: row => row.candidatures?.total ?? null },
  { id: 'a_traiter', header: 'Nouvelles candidatures', sortable: true, width: '8.5rem', wrapHeader: true, accessor: row => row.candidatures?.a_traiter ?? null, cellComponent: BadgeCell },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]

export const RECRUTEMENTS_ARCHIVES_COLUMNS: CspColumnDef<RecrutementsArchives>[] = [
  { id: 'intitule', header: 'Intitulé du recrutement', accessor: row => row.intitule, cellComponent: OffreIntituleCell },
  { id: 'reference_csp', header: 'Référence CSP', accessor: row => row.reference_csp },
  { id: 'responsables', header: 'Responsable', sortable: true, accessor: formatResponsablesLabel },
  { id: 'nature_offre', header: 'Nature du recrutement', accessor: formatNatureOffreLabel },
  { id: 'date_archivage', header: 'Date d\'archivage', sortable: true, accessor: row => row.date_archivage, cellComponent: ElapsedDaysCell },
  { id: 'recrute', header: 'Candidat recruté', accessor: row => row.recrute },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]
