import type { ProtoAgent } from '../data/mock'
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

export function formatAgentNom(agent: Pick<ProtoAgent, 'prenom' | 'nom'>): string {
  return `${agent.prenom} ${agent.nom}`.trim()
}

export function formatAgentNomAlphabetique(agent: Pick<ProtoAgent, 'prenom' | 'nom'>): string {
  return `${agent.nom} ${agent.prenom}`.trim()
}

export function formatListe(items: string[]): string {
  if (items.length <= 1)
    return items[0] ?? ''
  return `${items.slice(0, -1).join(', ')} et ${items.at(-1)}`
}
