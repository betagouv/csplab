import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { setupUser } from '@/test/render'
import CspSelectionSummary from './CspSelectionSummary.vue'

describe('cspSelectionSummary', () => {
  it('shows the scope and asks to edit the selection', async () => {
    const { emitted } = render(CspSelectionSummary, { props: { summary: '12 éléments' } })

    expect(screen.getByText('12 éléments')).toBeInTheDocument()
    await setupUser().click(screen.getByRole('button', { name: 'Modifier la sélection' }))

    expect(emitted().edit).toHaveLength(1)
  })

  it('shows the scope alone when the selection is fixed', () => {
    render(CspSelectionSummary, { props: { summary: 'Élément A', editable: false } })

    expect(screen.getByText('Élément A')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Modifier la sélection' })).not.toBeInTheDocument()
  })
})
