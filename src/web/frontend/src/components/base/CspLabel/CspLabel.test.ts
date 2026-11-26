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

  it('puts the class and style of the caller on the element that wraps the label and its dismiss button', () => {
    render(CspLabel, { props: { label: 'Libellé', dismissLabel: 'Retirer Libellé' }, attrs: { class: 'mise-en-page', style: 'margin: 4px' } })
    // eslint-disable-next-line testing-library/no-node-access -- the wrapper has no role: it only lays out the label and its dismiss button
    const wrapper = screen.getByRole('button', { name: 'Retirer Libellé' }).parentElement
    expect(wrapper).toHaveClass('mise-en-page')
    expect(wrapper).toHaveStyle({ margin: '4px' })
    expect(wrapper).toContainElement(screen.getByText('Libellé'))
  })
})
