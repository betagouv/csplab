import { describe, expect, it } from 'vitest'
import { navigationFor } from './navigation'

describe('navigationFor', () => {
  it('gives a staff user only the organismes management page', () => {
    const navigation = navigationFor(true)

    const items = navigation.flatMap(group => group.items)
    expect(items).toEqual([
      { icon: 'ri:settings-3-line', label: 'Gestion des organismes', to: 'organismes' },
    ])
  })

  it('gives a non-staff agent the full navigation', () => {
    const navigation = navigationFor(false)

    const items = navigation.flatMap(group => group.items.map(item => item.to))
    expect(items).toEqual(['mes-recrutements', 'organismes'])
  })
})
