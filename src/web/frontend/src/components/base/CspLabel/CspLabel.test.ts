import { render, screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { setupUser } from '@/test/render'
import CspLabel from './CspLabel.vue'

describe('cspLabel', () => {
  it('renders a button when clickable', async () => {
    const { emitted } = render(CspLabel, { props: { label: 'Libellé', clickable: true }, attrs: { 'aria-label': 'Modifier Libellé' } })
    const button = screen.getByRole('button', { name: 'Modifier Libellé' })
    expect(button).toHaveAttribute('type', 'button')
    await setupUser().click(button)
    expect(emitted().click).toHaveLength(1)
  })

  it('adds a dismiss button next to the label when it has a dismiss label', async () => {
    const onClick = vi.fn()
    const { emitted } = render(CspLabel, { props: { label: 'Libellé', clickable: true, dismissLabel: 'Retirer Libellé' }, attrs: { 'aria-label': 'Modifier Libellé', onClick } })
    await setupUser().click(screen.getByRole('button', { name: 'Retirer Libellé' }))
    expect(emitted().dismiss).toHaveLength(1)
    expect(onClick).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Modifier Libellé' })).toBeInTheDocument()
  })
})
