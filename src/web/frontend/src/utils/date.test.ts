import { describe, expect, it } from 'vitest'
import { calendarDaysBetween, formatDateLong, formatElapsedDays } from './date'

const NOW = new Date('2026-06-23T12:00:00')

function isoDaysAgo(days: number): string {
  const date = new Date(NOW)
  date.setDate(date.getDate() - days)
  return date.toISOString()
}

describe('calendarDaysBetween', () => {
  it('ignores intraday time', () => {
    expect(calendarDaysBetween(new Date('2026-03-22T23:00:00'), new Date('2026-03-23T01:00:00'))).toBe(1)
  })
})

describe('formatElapsedDays', () => {
  it('shows elapsed count from one day, today otherwise', () => {
    expect(formatElapsedDays(isoDaysAgo(0), NOW)).toBe('aujourd’hui')
    expect(formatElapsedDays(isoDaysAgo(1), NOW)).toBe('il y a 1 jour')
    expect(formatElapsedDays(isoDaysAgo(22), NOW)).toBe('il y a 22 jours')
  })

  it('returns - for invalid input', () => {
    expect(formatElapsedDays('not-a-date', NOW)).toBe('-')
  })
})

describe('formatDateLong', () => {
  it('formats ISO dates in french', () => {
    expect(formatDateLong('2026-05-02T10:00:00Z')).toBe('02 mai 2026')
  })

  it('returns - for invalid input', () => {
    expect(formatDateLong('not-a-date')).toBe('-')
  })
})
