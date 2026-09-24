import type { Person } from './types'

const weekdayDayMonth = new Intl.DateTimeFormat('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' })
const longWeekdayDayMonth = new Intl.DateTimeFormat('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
const dayMonth = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long' })
const dayMonthYear = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
const relative = new Intl.RelativeTimeFormat('fr', { numeric: 'auto' })

const MINUTE = 60 * 1000
const HOUR = 60 * MINUTE

function startOfDay(date: Date): number {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime()
}

function daysBetween(from: Date, to: Date): number {
  return Math.round((startOfDay(to) - startOfDay(from)) / (24 * HOUR))
}

export function formatTime(iso: string): string {
  const date = new Date(iso)
  const minutes = date.getMinutes()
  return minutes === 0
    ? `${date.getHours()} h`
    : `${date.getHours()} h ${String(minutes).padStart(2, '0')}`
}

function withFirst(formatted: string, iso: string): string {
  return new Date(iso).getDate() === 1 ? formatted.replace(/\b1\b/, '1er') : formatted
}

export function formatDay(iso: string): string {
  return withFirst(dayMonth.format(new Date(iso)), iso)
}

export function formatDayWithYear(iso: string): string {
  return withFirst(dayMonthYear.format(new Date(iso)), iso)
}

export function formatLongDay(iso: string): string {
  return withFirst(longWeekdayDayMonth.format(new Date(iso)), iso)
}

export function formatShortDay(iso: string): string {
  return withFirst(weekdayDayMonth.format(new Date(iso)), iso)
}

export function formatAbsolute(iso: string): string {
  return `${formatShortDay(iso)} à ${formatTime(iso)}`
}

export function formatSlot(iso: string): string {
  return `${formatLongDay(iso)} à ${formatTime(iso)}`
}

export function formatRelative(iso: string, now: Date): string {
  const date = new Date(iso)
  const elapsed = now.getTime() - date.getTime()
  if (elapsed < MINUTE)
    return 'à l’instant'
  if (elapsed < HOUR)
    return relative.format(-Math.round(elapsed / MINUTE), 'minute')
  const days = daysBetween(date, now)
  if (days === 0)
    return relative.format(-Math.round(elapsed / HOUR), 'hour')
  if (days === 1)
    return `hier à ${formatTime(iso)}`
  return relative.format(-days, 'day')
}

export function formatStamp(iso: string, now: Date, mode: 'relatives' | 'absolues'): string {
  return mode === 'relatives' ? formatRelative(iso, now) : formatAbsolute(iso)
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1_000_000)
    return `${Math.max(1, Math.round(bytes / 1000))} Ko`
  return `${(bytes / 1_000_000).toLocaleString('fr-FR', { maximumFractionDigits: 1 })} Mo`
}

export function fullName(person: Person): string {
  return `${person.prenom} ${person.nom}`
}
