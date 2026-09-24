import { describe, expect, it } from 'vitest'
import { calendarDaysBetween, formatDateLong, formatElapsedDays, formatElapsedTime } from './date'

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

describe('formatElapsedTime', () => {
  function isoMinutesAgo(minutes: number): string {
    return new Date(NOW.getTime() - minutes * 60 * 1000).toISOString()
  }

  it('climbs the unit as the delay grows', () => {
    expect(formatElapsedTime(isoMinutesAgo(0), NOW)).toBe('à l’instant')
    expect(formatElapsedTime(isoMinutesAgo(5), NOW)).toBe('il y a 5 minutes')
    expect(formatElapsedTime(isoMinutesAgo(60), NOW)).toBe('il y a 1 heure')
    expect(formatElapsedTime(isoDaysAgo(1), NOW)).toBe('hier')
    expect(formatElapsedTime(isoDaysAgo(6), NOW)).toBe('il y a 6 jours')
  })

  it('hands over to the date beyond a week, where relative stops helping', () => {
    expect(formatElapsedTime(isoDaysAgo(7), NOW)).toBe('16/06/26')
    expect(formatElapsedTime(isoDaysAgo(800), NOW)).toBe('14/04/24')
  })

  it('counts the hours of a message from today, not the elapsed days', () => {
    const lastNight = new Date('2026-06-23T02:00:00')
    expect(formatElapsedTime(new Date('2026-06-23T00:30:00').toISOString(), lastNight)).toBe('il y a 1 heure')
    expect(formatElapsedTime(new Date('2026-06-22T23:00:00').toISOString(), lastNight)).toBe('hier')
  })

  it('never counts backwards for a date in the future', () => {
    expect(formatElapsedTime(isoMinutesAgo(-5), NOW)).toBe('à l’instant')
  })

  it('returns - for invalid input', () => {
    expect(formatElapsedTime('not-a-date', NOW)).toBe('-')
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
