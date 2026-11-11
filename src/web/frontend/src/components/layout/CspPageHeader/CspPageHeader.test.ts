import { screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { renderWithApp } from '@/test/render'
import CspPageHeader from './CspPageHeader.vue'

describe('cspPageHeader', () => {
  it('names every link and button of a header with a back link', async () => {
    await renderWithApp(CspPageHeader, {
      props: { title: 'Titre de la page', backLink: { to: '/', label: 'Retour' } },
    })

    expect(screen.getByRole('link', { name: 'Retour' })).toHaveAttribute('href', '/')
    for (const control of [...screen.queryAllByRole('link'), ...screen.queryAllByRole('button')]) {
      expect(control).toHaveAccessibleName()
    }
  })
})
