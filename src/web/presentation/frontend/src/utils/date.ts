const PLACEHOLDER = '-'
const MS_PER_DAY = 1000 * 60 * 60 * 24

function startOfDay(date: Date): number {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime()
}

export function calendarDaysBetween(from: Date, to: Date): number {
  return Math.round((startOfDay(to) - startOfDay(from)) / MS_PER_DAY)
}

function parse(iso: string): Date | null {
  const date = new Date(iso)
  return Number.isNaN(date.getTime()) ? null : date
}

const autoDay = new Intl.RelativeTimeFormat('fr', { numeric: 'auto' })
const alwaysDay = new Intl.RelativeTimeFormat('fr', { numeric: 'always' })

export function formatElapsedDays(iso: string, now: Date = new Date()): string {
  const date = parse(iso)
  if (!date) {
    return PLACEHOLDER
  }
  const days = calendarDaysBetween(date, now)
  return days <= 0 ? autoDay.format(0, 'day') : alwaysDay.format(-days, 'day')
}
