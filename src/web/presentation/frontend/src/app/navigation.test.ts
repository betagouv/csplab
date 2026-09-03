import { describe, expect, it } from 'vitest'
import { navigationFor } from './navigation'

describe('navigationFor', () => {
  it('gives a staff user only the organismes management page', () => {
    expect(navigationFor(true)).toEqual([
      { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
    ])
  })

  it('gives a non-staff agent the full navigation', () => {
    const items = navigationFor(false).map(item => item.to)
    expect(items).toEqual(['mes-recrutements', 'organismes'])
  })
})
