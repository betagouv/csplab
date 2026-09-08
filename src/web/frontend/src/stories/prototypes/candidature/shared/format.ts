import type { ProtoActiviteType, ProtoCandidat } from '../data/mock'
import { formatElapsedDays } from '@/utils/date'

const relative = new Intl.RelativeTimeFormat('fr', { numeric: 'always' })

export function formatRelative(iso: string, now: Date = new Date()): string {
  const minutes = Math.round((now.getTime() - new Date(iso).getTime()) / 60_000)
  if (minutes < 1)
    return 'À l\'instant'
  if (minutes < 60)
    return `Il y a ${minutes} min`
  if (minutes < 24 * 60)
    return relative.format(-Math.round(minutes / 60), 'hour').replace(/^il y a/, 'Il y a')
  return formatElapsedDays(iso, now).replace(/^il y a/, 'Il y a')
}

export function formatCandidatNom(candidat: ProtoCandidat): string {
  return `${candidat.prenom} ${candidat.nom}`
}

export const ACTIVITE_ICONS: Record<ProtoActiviteType, string> = {
  reception: 'ri:inbox-2-line',
  etape: 'ri:arrow-left-right-line',
  note: 'ri:sticky-note-line',
  tag: 'ri:bookmark-line',
  message: 'ri:chat-3-line',
}
