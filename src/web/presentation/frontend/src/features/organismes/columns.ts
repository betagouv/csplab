import type { OrganismeAdmin } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import GestionnaireCell from './components/cells/GestionnaireCell.vue'
import OrganismeActionsCell from './components/cells/OrganismeActionsCell.vue'
import OrganismeNomCell from './components/cells/OrganismeNomCell.vue'

export const ORGANISMES_COLUMNS: CspColumnDef<OrganismeAdmin>[] = [
  { id: 'nom', header: 'Nom organisme', sortable: true, accessor: row => row.nom, cellComponent: OrganismeNomCell },
  { id: 'siret', header: 'SIRET', accessor: row => row.siret },
  { id: 'gestionnaire', header: 'Gestionnaire', cellComponent: GestionnaireCell },
  { id: 'gestion_candidatures', header: 'Recrutements sur l\'outil', accessor: row => row.gestion_candidatures ? 'Oui' : 'Non' },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OrganismeActionsCell },
]
