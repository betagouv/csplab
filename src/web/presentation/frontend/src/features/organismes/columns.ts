import type { CompteUtilisateur, OrganismeAdmin } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { formatElapsedDays } from '@/utils/date'
import CompteActionsCell from './components/cells/CompteActionsCell.vue'
import CompteTypeCell from './components/cells/CompteTypeCell.vue'
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

const shortDate = new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' })

export const COMPTES_UTILISATEURS_COLUMNS: CspColumnDef<CompteUtilisateur>[] = [
  { id: 'compte', header: 'Compte utilisateur', sortable: true, accessor: row => `${row.nom} ${row.prenom}` },
  { id: 'type', header: 'Type d\'utilisateur', cellComponent: CompteTypeCell },
  { id: 'poste', header: 'Poste', accessor: row => row.poste },
  { id: 'email', header: 'Courriel', accessor: row => row.email },
  { id: 'derniere_activite', header: 'Dernière activité', sortable: true, accessor: row => row.derniere_activite ? formatElapsedDays(row.derniere_activite) : '-' },
  { id: 'creation_compte', header: 'Création de compte', accessor: row => shortDate.format(new Date(row.creation_compte)) },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: CompteActionsCell },
]
