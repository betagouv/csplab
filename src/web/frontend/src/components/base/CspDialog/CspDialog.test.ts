import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import CspDialog from './CspDialog.vue'

describe('cspDialog', () => {
  it('names its close button in French by default', async () => {
    render(CspDialog, { props: { open: true, title: 'Titre' } })
    await nextTick()

    expect(screen.getByRole('button', { name: 'Fermer' })).toBeInTheDocument()
  })
})
