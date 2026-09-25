const PLACEHOLDER = '-'
const MS_PER_MINUTE = 1000 * 60
const MS_PER_HOUR = MS_PER_MINUTE * 60
const MS_PER_DAY = MS_PER_HOUR * 24

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

const autoRelative = new Intl.RelativeTimeFormat('fr', { numeric: 'auto' })
const alwaysRelative = new Intl.RelativeTimeFormat('fr', { numeric: 'always' })

export const shortDate = new Intl.DateTimeFormat('fr-FR', {
  day: '2-digit',
  month: '2-digit',
  year: '2-digit',
})

const longDate = new Intl.DateTimeFormat('fr-FR', {
  day: '2-digit',
  month: 'long',
  year: 'numeric',
})

export function formatElapsedDays(iso: string, now: Date = new Date()): string {
  const date = parse(iso)
  if (!date) {
    return PLACEHOLDER
  }
  const days = calendarDaysBetween(date, now)
  return days <= 0 ? autoRelative.format(0, 'day') : alwaysRelative.format(-days, 'day')
}

const ELAPSED_DAYS_LIMIT = 7

export function formatElapsedTime(iso: string, now: Date = new Date()): string {
  const date = parse(iso)
  if (!date) {
    return PLACEHOLDER
  }
  const elapsed = Math.max(now.getTime() - date.getTime(), 0)
  if (elapsed < MS_PER_MINUTE) {
    return 'à l’instant'
  }
  if (elapsed < MS_PER_HOUR) {
    return alwaysRelative.format(-Math.floor(elapsed / MS_PER_MINUTE), 'minute')
  }

  const days = calendarDaysBetween(date, now)
  if (days <= 0) {
    return alwaysRelative.format(-Math.floor(elapsed / MS_PER_HOUR), 'hour')
  }
  if (days >= ELAPSED_DAYS_LIMIT) {
    return shortDate.format(date)
  }
  return days === 1 ? autoRelative.format(-1, 'day') : alwaysRelative.format(-days, 'day')
}

export function formatDateLong(iso: string): string {
  const date = parse(iso)
  if (!date) {
    return PLACEHOLDER
  }
  return longDate.format(date)
}
