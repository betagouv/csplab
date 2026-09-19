import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import CspDrawer from './CspDrawer.vue'

describe('cspDrawer', () => {
  it('names its close button in French by default', async () => {
    render(CspDrawer, { props: { open: true, title: 'Titre' } })
    await nextTick()

    expect(screen.getByRole('button', { name: 'Fermer' })).toBeInTheDocument()
  })
})
