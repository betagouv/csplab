import type { AgentOrganisme, OrganismesList } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import ElapsedDaysCell from '@/components/base/CspDataTable/cells/ElapsedDaysCell.vue'
import { shortDate } from '@/utils/date'
import AgentActionsCell from './components/cells/AgentActionsCell.vue'
import OrganismeActionsCell from './components/cells/OrganismeActionsCell.vue'
import OrganismeNomCell from './components/cells/OrganismeNomCell.vue'

import { formatAgentNameAlphabetical, formatAgentRole } from './format'

export const ORGANISMES_LIST_COLUMNS: CspColumnDef<OrganismesList>[] = [
  { id: 'nom', header: 'Nom organisme', sortable: true, accessor: row => row.nom, cellComponent: OrganismeNomCell },
  { id: 'siret', header: 'SIRET', width: '9.5rem', accessor: row => row.siret },
  { id: 'gestionnaire', header: 'Gestionnaire', sortable: true, width: '11rem', accessor: row => row.gestionnaire },
  { id: 'gestion_ats', header: 'Recrutements sur l\'outil', width: '8.5rem', wrapHeader: true, accessor: row => row.gestion_ats ? 'Oui' : 'Non' },
  { id: 'date_derniere_activite', header: 'Dernière activité', sortable: true, width: '9.5rem', wrapHeader: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'nombre_agents', header: 'Nombre d\'agents', align: 'end', width: '7rem', wrapHeader: true, accessor: row => row.nombre_agents },
  { id: 'nombre_offres_publiees', header: 'Nombre de recrutements', align: 'end', width: '8.5rem', wrapHeader: true, accessor: row => row.nombre_offres_publiees },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OrganismeActionsCell },
]

export const ORGANISME_AGENTS_COLUMNS: CspColumnDef<AgentOrganisme>[] = [
  { id: 'agent', header: 'Membre', sortable: true, accessor: row => formatAgentNameAlphabetical(row) },
  { id: 'role', header: 'Rôle', accessor: row => formatAgentRole(row.role) },
  { id: 'poste', header: 'Poste', accessor: row => row.poste },
  { id: 'email', header: 'Courriel', accessor: row => row.email },
  { id: 'date_derniere_activite', header: 'Dernière activité', sortable: true, width: '9.5rem', wrapHeader: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'date_creation_compte', header: 'Création de compte', accessor: row => shortDate.format(new Date(row.date_creation_compte)) },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: AgentActionsCell },
]
