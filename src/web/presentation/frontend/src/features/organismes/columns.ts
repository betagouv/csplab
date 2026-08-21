import type { AgentOrganisme, OrganismesList } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import ElapsedDaysCell from '@/features/organismes/components/cells/ElapsedDaysCell.vue'
import OrganismeActionsCell from './components/cells/OrganismeActionsCell.vue'
import OrganismeNomCell from './components/cells/OrganismeNomCell.vue'
import { ROLE_LABELS } from './constants/organisme'

export const ORGANISMES_LIST_COLUMNS: CspColumnDef<OrganismesList>[] = [
  { id: 'nom', header: 'Nom organisme', sortable: true, accessor: row => row.nom, cellComponent: OrganismeNomCell },
  { id: 'siret', header: 'SIRET', accessor: row => row.siret },
  { id: 'gestionnaire', header: 'Gestionnaire', sortable: true, accessor: row => row.gestionnaire ?? '-' },
  { id: 'gestion_ats', header: 'Recrutements sur l\'outil', accessor: row => row.gestion_ats ? 'Oui' : 'Non' },
  { id: 'date_derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'nombre_agents', header: 'Nombre d\'agents', accessor: row => row.nombre_agents ?? '-' },
  { id: 'nombre_offres_publiees', header: 'Nombre de recrutements', accessor: row => row.nombre_offres_publiees ?? '-' },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OrganismeActionsCell },
]

const shortDate = new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' })

export const ORGANISME_AGENTS_COLUMNS: CspColumnDef<AgentOrganisme>[] = [
  { id: 'agent', header: 'Membre', sortable: true, accessor: row => `${row.nom} ${row.prenom}` },
  { id: 'role', header: 'Rôle', accessor: row => ROLE_LABELS[row.role as keyof typeof ROLE_LABELS] ?? row.role },
  { id: 'poste', header: 'Poste', accessor: row => row.poste },
  { id: 'email', header: 'Courriel', accessor: row => row.email },
  { id: 'date_derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.date_derniere_activite, cellComponent: ElapsedDaysCell },
  { id: 'date_creation_compte', header: 'Création de compte', accessor: row => shortDate.format(new Date(row.date_creation_compte)) },
]
