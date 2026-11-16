import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import UnreadConversationsCell from './components/cells/UnreadConversationsCell.vue'

export const UNREAD_CONVERSATIONS_COLUMN: CspColumnDef<{ unread_conversations: number }> = {
  id: 'unread_conversations',
  header: 'Nouveau message',
  accessor: row => row.unread_conversations,
  cellComponent: UnreadConversationsCell,
}
