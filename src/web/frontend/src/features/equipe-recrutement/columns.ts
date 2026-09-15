import type { MembreEquipe } from './types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import AgentNomCell from '@/features/organismes/components/cells/AgentNomCell.vue'
import MembreActionsCell from './components/cells/MembreActionsCell.vue'
import { formatMembreNameAlphabetical, formatRecrutementRole } from './format'

export const EQUIPE_RECRUTEMENT_COLUMNS: CspColumnDef<MembreEquipe>[] = [
  { id: 'membre', header: 'Membre', sortable: true, width: '16rem', accessor: row => formatMembreNameAlphabetical(row), cellComponent: AgentNomCell },
  { id: 'role', header: 'Rôle', sortable: true, width: '10rem', accessor: row => formatRecrutementRole(row.recrutement_role) },
  { id: 'poste', header: 'Poste', accessor: row => row.poste },
  { id: 'email', header: 'Courriel', accessor: row => row.email },
]

export const EQUIPE_RECRUTEMENT_ACTIONS_COLUMN: CspColumnDef<MembreEquipe> = {
  id: 'actions',
  header: '',
  align: 'end',
  width: '3.5rem',
  cellComponent: MembreActionsCell,
}
