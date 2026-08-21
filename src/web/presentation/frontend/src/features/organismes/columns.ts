import type { OrganismesList } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import ElapsedDaysCell from '@/features/organismes/components/cells/ElapsedDaysCell.vue'
import OrganismeNomCell from './components/cells/OrganismeNomCell.vue'

export const ORGANISMES_LIST_COLUMNS: CspColumnDef<OrganismesList>[] = [
  { id: 'nom', header: 'Nom organisme', sortable: true, accessor: row => row.nom, cellComponent: OrganismeNomCell },
  { id: 'siret', header: 'SIRET', accessor: row => row.siret },
  { id: 'gestionnaire', header: 'Gestionnaire', sortable: true, accessor: row => row.gestionnaire ?? '-' },
  { id: 'gestion_ats', header: 'Recrutements sur l\'outil', accessor: row => row.gestion_ats ? 'Oui' : 'Non' },
  { id: 'date_derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'nombre_agents', header: 'Nombre d\'agents', accessor: row => row.nombre_agents ?? '-' },
  { id: 'nombre_offres_publiees', header: 'Nombre de recrutements', accessor: row => row.nombre_offres_publiees ?? '-' },
]
