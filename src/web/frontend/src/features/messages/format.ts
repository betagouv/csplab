import { pluralize } from '@/utils/format'

export function formatUnreadConversations(count: number): string {
  return count
    ? `${count} ${pluralize(count, 'conversation')} non ${pluralize(count, 'lue')}`
    : 'Aucune conversation non lue'
}
