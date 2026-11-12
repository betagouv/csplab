import { render, screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { setupUser } from '@/test/render'
import CspLabel from './CspLabel.vue'

function labelRoot(): HTMLElement {
  const root = screen.getByText('Libellé').closest<HTMLElement>('.csp-label')
  if (!root) {
    throw new Error('label root not found')
  }
  return root
}

describe('cspLabel', () => {
  it('reads the palette roles of its color', () => {
    render(CspLabel, { props: { label: 'Libellé', color: 'mint' } })
    expect(labelRoot().style.getPropertyValue('--csp-label-background')).toBe('var(--csp-palette-mint-background)')
    expect(labelRoot().style.getPropertyValue('--csp-label-text')).toBe('var(--csp-palette-mint-text)')
    expect(labelRoot().style.getPropertyValue('--csp-label-dot')).toBe('var(--csp-palette-mint-dot)')
  })

  it('draws a border by default, and none when bordered is false', async () => {
    const { rerender } = render(CspLabel, { props: { label: 'Libellé' } })
    expect(labelRoot()).toHaveClass('csp-label--bordered')
    await rerender({ label: 'Libellé', bordered: false })
    expect(labelRoot()).not.toHaveClass('csp-label--bordered')
  })

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

  it('keeps the class and style of the caller on the label', () => {
    render(CspLabel, { props: { label: 'Libellé', clickable: true }, attrs: { class: 'mise-en-page', style: 'margin: 4px' } })
    expect(labelRoot()).toHaveClass('mise-en-page')
    expect(labelRoot().style.margin).toBe('4px')
  })
})
